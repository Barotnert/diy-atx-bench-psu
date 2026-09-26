"""Check exported net connectivity and local report links; never certifies hardware."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import re
import math
from urllib.parse import unquote
from calculate import calculate

ROOT=Path(__file__).resolve().parents[1]
(ROOT/'docs/verification.json').write_text(json.dumps({'status':'IN PROGRESS OR FAILED; do not treat this as a pass','physical_tests':'Reported PASS; numerical records unavailable'})+'\n',encoding='utf8')
checks=[]
def require(ok,message):
    if not ok: raise AssertionError(message)
    checks.append(message)

erc=json.loads((ROOT/'hardware/erc.json').read_text(encoding='utf8'))
violations=[v for sheet in erc['sheets'] for v in sheet['violations']]
require(not violations,'KiCad ERC: zero errors and warnings')
tree=ET.parse(ROOT/'hardware/diy_atx_psu.net')
pin_net={}
for net in tree.findall('.//nets/net'):
    for n in net.findall('node'):
        pin_net[(n.attrib['ref'],n.attrib['pin'])]=net.attrib['name']
def net(ref,pin):return pin_net[(ref,str(pin))]
def same(*pins): return len({net(*p) for p in pins})==1
def linked(p,name):return net(*p).lstrip('/')==name
expected={1:'+3V3_RAW',2:'+3V3_RAW',3:'COM',4:'+5V_RAW',5:'COM',6:'+5V_RAW',7:'COM',8:'PWR_OK',9:'+5VSB_RAW',10:'+12V_RAW',11:'+12V_RAW',12:'+3V3_RAW',13:'+3V3_RAW',14:'-12V_RAW',15:'COM',16:'PS_ON_N',17:'COM',18:'COM',19:'COM',21:'+5V_RAW',22:'+5V_RAW',23:'+5V_RAW',24:'COM'}
for p,n in expected.items():
    if p!=14: require(linked(('J1',p),n),f'ATX pin {p}: {n}')
require(len({net('J1',p) for p in [1,4,9,10,3]})==5,'Used raw rails, standby and COM remain distinct')
require('unconnected' in net('J1',14),'Unused -12V source pin has no external branch')
for f,p,j,jn in [('F1',10,'J2',1),('F2',4,'J3',1),('F3',1,'J4',1)]:
    require(same(('J1',p),(f,1)),f'{f} input is on intended source rail')
    require(same((f,2),(j,jn)),f'{f} output supplies intended branch')
    require(net(f,1)!=net(f,2),f'{f} is not bypassed by a wire/net label')
require(same(('SW1',1),('J1',16)) and same(('SW1',2),('J1',3)),'PS_ON switch spans PS_ON_N and COM')
require(same(('U1',2),('J5',1),('J1',3)),'Converter input return and fixed COM are connected')
require(same(('U1',3),('F4',1)) and same(('F4',2),('J6',1)) and same(('U1',4),('J7',1)),'Adjustable branch model routes OUT+ through F4 and returns to OUT-')
require(len({net('U1',3),net('U1',4),net('J5',1)})==3,'ADJ_POS, ADJ_NEG and fixed COM are separate external nets')
require(same(('R1',2),('D1',2)) and same(('D1',1),('J5',1)),'Green resistor feeds LED anode; cathode returns COM')
require(same(('R2',1),('J1',8)) and same(('R2',2),('D2',2)) and same(('D2',1),('J5',1)),'Red LED has series resistor and correct proposed return')
require(same(('TP1',1),('J1',8)),'PWR_OK goes to a dedicated test point')
components={c.attrib['ref']:c.findtext('value') for c in tree.findall('.//components/comp')}
design=json.loads((ROOT/'hardware/protection-design.json').read_text(encoding='utf8'))
for b in design['branches']:
    require(components[b['ref']]=="Fuse",f"{b['ref']} is identified without an unverified installed rating")
    require(b['assumed_continuous_A']<=design['loading_factor']*b['candidate_fuse_A'],f"{b['ref']} meets preliminary continuous-loading assumption")
require({r for r in components if re.fullmatch(r'F[0-9]+',r)}=={'F1','F2','F3','F4'},'Three fixed-output fuses and one adjustable-output fuse in the circuit model')
for ref,pin in [('U1',10),('J8',10),('J9',4),('R1',9),('R2',8)]:
    require(same((ref,1),('J1',pin)),f'{ref} uses its source rail without an added branch fuse')
require(not any(ref=='M1' for ref,pin in pin_net),'Original PSU fan is a functional block without guessed supply wires')
require(net('F4',1)!=net('F4',2),'Adjustable fuse F4 is not bypassed by a net label')
require('J10' not in components,'No unfitted -12V output terminal in the main drawing')
require(all(components[r].startswith('1k') for r in ['R1','R2']),'Both proposed LED resistors are 1k')
d=calculate()
require(math.isclose(d['red_PWR_OK_5V_ideal']['resistor_power_mW'],9),'Red LED ideal 5V resistor loss is 9 mW; signal voltage is not guaranteed')
require(math.isclose(d['red_PWR_OK_5V_ideal']['current_mA']/d['pwr_ok_source_test_current_mA'],15),'Ideal red LED demand exceeds PWR_OK specified sourcing test load by 15 times')
require(net('R2',1)!=net('J1',10),'Red LED is on PWR_OK, not the 12V power rail')
require(math.isclose(d['wire_example']['drop_V'],0.07),'Round-trip wire drop is 70 mV at assumed 3 A')
require(math.isclose(d['converter_24V_1A_at_12V']['input_W']-d['converter_24V_1A_at_12V']['output_W'],d['converter_24V_1A_at_12V']['loss_W']),'Converter input/output/loss energy balance')
link_count=0
for p in ROOT.rglob('*.md'):
    if any(part in {'tmp','.git','references'} for part in p.relative_to(ROOT).parts):continue
    text=p.read_text(encoding='utf8')
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
        if target.startswith(('https://','http://','#','mailto:')):continue
        path=unquote(target.split('#')[0].strip('<>'))
        require((p.parent/path).exists(),f'Local link exists: {p.relative_to(ROOT)} -> {path}')
        link_count+=1
for p in [ROOT/'.vscode/tasks.json',ROOT/'.vscode/settings.json',ROOT/'DIY-ATX-PSU.code-workspace']:
    json.loads(p.read_text(encoding='utf8'))
require(len(list((ROOT/'docs/images').glob('IMG_*.jpg')))==26,'All 26 supplied HEIC photographs have browser-readable JPEG copies')
test_record=json.loads((ROOT/'docs/evidence/test-results.json').read_text(encoding='utf8'))
require(len(test_record['results'])==10 and all(r['basis']=='reported' for r in test_record['results']),'Test summary preserves the reported basis')
require(test_record.get('numerical_readings') is None and test_record.get('test_photographs') is None,'No numerical measurements or test photographs fabricated')
for path in [ROOT/'README.md',*ROOT.glob('docs/*.md')]:
    require(not re.search('[\u0E00-\u0E7F]',path.read_text(encoding='utf8')),f'English report text: {path.relative_to(ROOT)}')
result={'status':'PASS: DOCUMENT/NETLIST CHECKS ONLY','kicad_version':erc.get('kicad_version'),'checks_passed':len(checks),'local_links_checked':link_count,'physical_tests':'Team-reported qualitative PASS summary','scope':'Schematic connectivity, calculation consistency and document links.','checks':checks}
(ROOT/'docs/verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(f"PASS: {len(checks)} document/connectivity checks; {link_count} local links. Prototype results are reported separately.")
