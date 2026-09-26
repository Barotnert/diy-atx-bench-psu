"""Package the tracked project files, excluding local/private material."""
from pathlib import Path
import subprocess
import zipfile
ROOT=Path(__file__).resolve().parents[1]
names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf8').split('\0')
files=[ROOT/n for n in names if n and (ROOT/n).is_file()]
for p in files:
    rel=p.relative_to(ROOT)
    if any(x in {'.git','tmp','references','submission','.history','__pycache__'} for x in rel.parts):
        raise RuntimeError(f'Private or temporary path unexpectedly tracked: {rel}')
dest=ROOT/'submission/DIY-ATX-PSU_Project-Report.zip'
dest.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,Path('DIY-ATX-PSU')/p.relative_to(ROOT))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert z.read('DIY-ATX-PSU/README.md')==(ROOT/'README.md').read_bytes()
    assert z.read('DIY-ATX-PSU/hardware/diy_atx_psu.kicad_sch')==(ROOT/'hardware/diy_atx_psu.kicad_sch').read_bytes()
print(f'Packaged {len(files)} files; ZIP integrity and current README/schematic verified. {dest.name}')
