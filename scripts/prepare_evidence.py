"""Convert user-provided HEIC photos and build a traceable evidence index.
Requires Pillow + pillow-heif; original files are read only.
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    args=ap.parse_args()
    from PIL import Image,ImageOps
    import pillow_heif
    pillow_heif.register_heif_opener()
    out=ROOT/'docs/images';out.mkdir(parents=True,exist_ok=True)
    notes={'IMG_4303': 'Enclosure and illuminated LED strip.', 'IMG_4305': 'Heat-shrink sleeve and insulation material.', 'IMG_4306': 'Fuse-holder cap.', 'IMG_4307': 'Green LED parts.', 'IMG_4308': 'Red LED parts.', 'IMG_4309': 'Drill press used during construction.', 'IMG_4310': 'Component parts in packaging.', 'IMG_4311': 'Construction consumable bottle.', 'IMG_4312': 'Rocker switch part.', 'IMG_4313': 'Blue binding-post part.', 'IMG_4314': 'Front panel with fixed terminals, fuse holders, ZK-4KX and adjustable terminals.', 'IMG_4315': 'Red binding-post part.', 'IMG_4316': 'Panel fuse-holder part.'}
    manifest=[];rows=[]
    for f in sorted(args.source.glob('IMG_*.HEIC')):
        dest=out/(f.stem+'.jpg')
        im=ImageOps.exif_transpose(Image.open(f)).convert('RGB');original_size=list(im.size)
        im.thumbnail((1800,1800));im.save(dest,quality=88)
        note=notes.get(f.stem,'Internal construction view: PSU board, wiring and mechanical arrangement.')
        manifest.append({'original_filename':f.name,'original_sha256':sha(f),'original_oriented_pixels':original_size,'derived_file':dest.relative_to(ROOT).as_posix(),'derived_sha256':sha(dest),'derived_pixels':list(im.size),'observation':note})
        rows.append(f'| [{f.stem}](images/{f.stem}.jpg) | {note} |')
    (ROOT/'docs/evidence').mkdir(exist_ok=True)
    (ROOT/'docs/evidence/source-manifest.json').write_text(json.dumps({'revision':'1.0','count':len(manifest),'method':'EXIF orientation applied; RGB JPEG quality 88; max 1800x1800; no copied EXIF; originals unchanged','photos':manifest},indent=2)+'\n',encoding='utf8')
    header='# Construction Photographs\n\nThe photographs show the parts and assembly process. Internal views were taken during construction; the project enclosure is now closed. The [photo manifest](evidence/source-manifest.json) records image identifiers and file hashes.\n\n| Photograph | Description |\n|---|---|\n'
    tail="\n\n[Functional test summary](testing.md)\n"
    (ROOT/'docs/evidence-register.md').write_text(header+'\n'.join(rows)+tail,encoding='utf8')
    print(f'Prepared {len(manifest)} photos and their evidence index.')
if __name__=='__main__':main()
