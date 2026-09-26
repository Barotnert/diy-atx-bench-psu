"""Generate the external wiring schematic from the reported connections. Python 3, standard library only.

This is a wiring document, not a PCB or reverse-engineered PSU design.
Custom module/connector pins are passive abstractions: ERC cannot certify hardware.
"""
from pathlib import Path
import json
import uuid

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / 'hardware'
HW.mkdir(exist_ok=True)
protection=json.loads((HW/'protection-design.json').read_text(encoding='utf8'))
fuse_ratings={b['ref']:b['candidate_fuse_A'] for b in protection['branches']}
def uid(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'diy-atx-psu/r0.1/' + key))
def q(s):
    return json.dumps(str(s), ensure_ascii=False)
def effects(size=1.27, justify=''):
    return f'(effects (font (size {size} {size})) {justify})'
def pin(n, name, x, y, angle, length=5.08):
    return f'(pin passive line (at {x} {y} {angle}) (length {length}) (name {q(name)} {effects()}) (number {q(n)} {effects(1.0)}))'
def rect(x1,y1,x2,y2):
    return f'(rectangle (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.254) (type default)) (fill (type background)))'
def line(*pts):
    return '(polyline (pts '+ ' '.join(f'(xy {x} {y})' for x,y in pts)+') (stroke (width 0.254) (type default)) (fill (type none)))'
def lib(name, ref, body, pins):
    return f'''(symbol {q(name)} (pin_names (offset 1.016)) (in_bom yes) (on_board no)
    (property "Reference" {q(ref)} (at 0 7.62 0) {effects()})
    (property "Value" {q(name)} (at 0 -7.62 0) {effects()})
    (symbol {q(name+'_0_1')} {body})
    (symbol {q(name+'_1_1')} {' '.join(pins)}))'''
libs = {}
libs['R'] = lib('R','R',rect(-2.54,1.27,2.54,-1.27),[pin(1,'',-7.62,0,0),pin(2,'',7.62,0,180)])
libs['Fuse'] = lib('Fuse','F',rect(-2.54,1.27,2.54,-1.27)+line((-2.54,0),(2.54,0)),[pin(1,'',-7.62,0,0),pin(2,'',7.62,0,180)])
libs['LED'] = lib('LED','D',line((-2.54,2.54),(-2.54,-2.54),(2.54,0),(-2.54,2.54))+line((2.54,2.54),(2.54,-2.54))+line((0,3.81),(2.54,6.35),(1.27,6.35))+line((2.54,3.81),(5.08,6.35),(3.81,6.35)),[pin(2,'A',-7.62,0,0),pin(1,'K',7.62,0,180)])
libs['Switch'] = lib('Switch','SW',line((-2.54,0),(2.54,2.54)),[pin(1,'',-7.62,0,0),pin(2,'',7.62,0,180)])
libs['Post'] = lib('Post','J','(circle (center 0 0) (radius 1.27) (stroke (width 0.254) (type default)) (fill (type none)))',[pin(1,'',-5.08,0,0,3.81)])
libs['FanAssembly'] = lib('FanAssembly','M',rect(-15.24,5.08,15.24,-5.08),[])
libs['Load2'] = lib('Load2','J',rect(-7.62,5.08,7.62,-5.08),[pin(1,'+',-12.7,2.54,0),pin(2,'-',-12.7,-2.54,0)])
libs['ZK4KX'] = lib('ZK4KX','U',rect(-15.24,10.16,15.24,-10.16),[pin(1,'IN+',-20.32,5.08,0),pin(2,'IN-',-20.32,-5.08,0),pin(3,'OUT+',20.32,5.08,180),pin(4,'OUT-',20.32,-5.08,180)])
signals = ['+3V3_RAW','+3V3_RAW','COM','+5V_RAW','COM','+5V_RAW','COM','PWR_OK','+5VSB_RAW','+12V_RAW','+12V_RAW','+3V3_RAW','+3V3_RAW','-12V_RAW','COM','PS_ON_N','COM','COM','COM','RESERVED','+5V_RAW','+5V_RAW','+5V_RAW','COM']
libs['ATX24_LOGICAL'] = lib('ATX24_LOGICAL','J',rect(-20.32,5.08,20.32,-121.92),[pin(i+1,s,25.4,-i*5.08,180) for i,s in enumerate(signals)])
library = '(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+'\n'.join(libs.values())+'\n)\n'
(HW/'Project.kicad_sym').write_text(library,encoding='utf8')
(HW/'sym-lib-table').write_text('(sym_lib_table (lib (name "Project") (type "KiCad") (uri "${KIPRJMOD}/Project.kicad_sym") (options "") (descr "Project wiring symbols; logical pin maps")))\n',encoding='utf8')
elements=[]
count=0
manifest={}
pin_positions=set()
def add(s): elements.append(s)
def wire(a,b):
    global count
    count+=1
    add(f'(wire (pts (xy {a[0]:.4f} {a[1]:.4f}) (xy {b[0]:.4f} {b[1]:.4f})) (stroke (width 0) (type default)) (uuid {uid("wire"+str(count))}))')
def label(net,x,y):
    global count
    count+=1
    add(f'(label {q(net)} (at {x:.4f} {y:.4f} 0) {effects(1.0,"(justify left bottom)")} (uuid {uid("label"+str(count))}))')
def text(s,x,y,size=1.27):
    global count
    count+=1
    add(f'(text {q(s)} (at {x} {y} 0) {effects(size,"(justify left top)")} (uuid {uid("text"+str(count))}))')
def comp(kind,ref,val,x,y):
    manifest[ref]={'symbol':kind,'value':val}
    offsets={'FanAssembly':[],'R':[(-7.62,0),(7.62,0)],'Fuse':[(-7.62,0),(7.62,0)],'LED':[(-7.62,0),(7.62,0)],'Switch':[(-7.62,0),(7.62,0)],'Post':[(-5.08,0)],'Load2':[(-12.7,-2.54),(-12.7,2.54)],'ZK4KX':[(-20.32,-5.08),(-20.32,5.08),(20.32,-5.08),(20.32,5.08)],'ATX24_LOGICAL':[(25.4,i*5.08) for i in range(24)]}
    pin_positions.update((round(x+dx,4),round(y+dy,4)) for dx,dy in offsets[kind])
    add(f'''(symbol (lib_id "Project:{kind}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board no) (dnp no) (uuid {uid(ref)})
    (property "Reference" {q(ref)} (at {x} {y-7.62} 0) {effects(1.0)})
    (property "Value" {q(val)} (at {x} {y+7.62} 0) {effects(1.0)})
    (instances (project "diy_atx_psu" (path "/{uid('root')}" (reference {q(ref)}) (unit 1)))))''')
def netwire(net,a,b):
    wire(a,b)
    endpoint=b if (round(a[0],4),round(a[1],4)) in pin_positions else a
    label(net,*endpoint)
def fuse(ref,raw,out,x,y):
    comp('Fuse',ref,'Fuse',x,y)
    netwire(raw,(x-27.94,y),(x-7.62,y)); netwire(out,(x+7.62,y),(x+27.94,y))
def post(ref,val,net,x,y):
    comp('Post',ref,val,x,y); netwire(net,(x-20.32,y),(x-5.08,y))

text('DIY ATX BENCH POWER SUPPLY | REV 1.5',15.24,13.97,2.0)
text('Project 1 - Electronics Circuits Laboratory',15.24,21.59)
text('A. ATX SUPPLY SIGNALS',15.24,27.94,1.5)
comp('ATX24_LOGICAL','J1','ATX SIGNAL MAP ONLY',38.1,45.72)
for i,s in enumerate(signals):
    x=63.5; y=45.72+i*5.08
    if s in {'RESERVED','-12V_RAW'}: add(f'(no_connect (at {x} {y}) (uuid {uid("nc"+str(i+1))}))')
    else: netwire(s,(x,y),(x+17.78,y))
text('PSU1: PLENTY COMPUTER ATX500WS.\nPin numbers: standard 24-pin ATX signal reference.\nCOM is the common supply return.',15.24,175.26)
post('TP1','PWR_OK TEST','PWR_OK',91.44,195.58)
text('B. FIXED OUTPUTS / SEPARATE FUSES',111.76,27.94,1.5)
for f,raw,out,j,v,y in [('F1','+12V_RAW','+12V_POST','J2','RED +12V',45.72),('F2','+5V_RAW','+5V_POST','J3','YELLOW +5V',71.12),('F3','+3V3_RAW','+3V3_POST','J4','GREEN +3.3V',96.52)]:
    fuse(f,raw,out,149.86,y); post(j,v,out,226.06,y)
post('J5','BLACK COM','COM',226.06,147.32)
text('F1: 12 V output    F2: 5 V output    F3: 3.3 V output\nFixed outputs share the COM terminal.',111.76,162.56)
text('C. SOCKET, STRIP AND FAN',259.08,27.94,1.5)
for raw,j,val,y in [('+12V_RAW','J8','12V CIG. SOCKET',45.72),('+5V_RAW','J9','5V LED STRIP',86.36)]:
    comp('Load2',j,val,373.38,y+2.54)
    netwire(raw,(292.1,y),(360.68,y))
    netwire('COM',(337.82,y+5.08),(360.68,y+5.08))
comp('FanAssembly','M1','ORIGINAL PSU FAN',373.38,129.54)
text('J8: 12 V panel-mount cigarette-lighter power socket.\nCentre contact: +12 V. Outer contact: COM.\nJ9: 5 V LED strip, direct PSU output supply.\nM1: original fan circuit inside PSU1.',259.08,149.86)
text('D. ADJUSTABLE OUTPUT / SEPARATE RETURN',111.76,185.42,1.5)
comp('ZK4KX','U1','ZK-4KX MODULE',213.36,210.82)
netwire('+12V_RAW',(149.86,205.74),(193.04,205.74))
netwire('COM',(180.34,215.9),(193.04,215.9))
netwire('ADJ_CONV_POS',(233.68,205.74),(248.92,205.74)); netwire('ADJ_NEG',(233.68,215.9),(248.92,215.9))
comp('Fuse','F4','Fuse',266.7,200.66)
netwire('ADJ_CONV_POS',(241.3,200.66),(259.08,200.66))
post('J6','ADJ +','ADJ_POS',294.64,200.66); post('J7','ADJ - / NOT COM','ADJ_NEG',284.48,226.06)
text('U1: ZK-4KX buck-boost module.\nLoad return connects to OUT-.\nSeparate return; non-isolated output.',111.76,238.76)
text('E. MAIN SWITCH',15.24,205.74,1.5)
comp('Switch','SW1','MAINTAINED PS_ON',53.34,223.52)
netwire('PS_ON_N',(22.86,223.52),(45.72,223.52)); netwire('COM',(60.96,223.52),(83.82,223.52))
text('SW1 closed: main outputs ON.\nSW1 open: main outputs OFF.\nStandby supply remains active while AC is connected.',15.24,241.3)
text('F. STANDBY AND MAIN INDICATORS',307.34,175.26,1.5)
text('D1: green, purple +5VSB wire.\nD2: red, gray PWR_OK wire.',307.34,195.58)
for ref,d,net,val,y in [('R1','D1','+5VSB_RAW','GREEN / SB',218.44),('R2','D2','PWR_OK','RED / PWR_OK',241.3)]:
    comp('R',ref,'1k',325.12,y); comp('LED',d,val,375.92,y)
    netwire(net,(302.26,y),(317.5,y)); wire((332.74,y),(368.3,y)); netwire('COM',(383.54,y),(396.24,y))
text('Green indicates standby power; red follows PWR_OK.\nSignal loading and fuse selection: see report calculations.',111.76,264.16,1.27)

embedded=[]
for name,s in libs.items(): embedded.append(s.replace(f'(symbol "{name}"',f'(symbol "Project:{name}"',1))
doc=f'''(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0") (uuid {uid('root')}) (paper "A3")
(title_block (title "DIY ATX Bench Power Supply") (date "2026-09-26") (rev "1.5"))
(lib_symbols {' '.join(embedded)})
{chr(10).join(elements)}
(embedded_fonts no))\n'''
(HW/'diy_atx_psu.kicad_sch').write_text(doc,encoding='utf8')
if not (HW/'diy_atx_psu.kicad_pro').exists():
    (HW/'diy_atx_psu.kicad_pro').write_text(json.dumps({'meta':{'filename':'diy_atx_psu.kicad_pro','version':1},'text_variables':{}},indent=2)+'\n',encoding='utf8')
(HW/'component_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
print('Generated schematic, local symbol library, project and component manifest.')
