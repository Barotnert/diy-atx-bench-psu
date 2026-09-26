# Project Files

Open `DIY-ATX-PSU.code-workspace` in VS Code. Open `README.md` and use Ctrl+Shift+V for the report preview. GitHub renders the relative image links and Mermaid block diagram.

Open `hardware/diy_atx_psu.kicad_pro` in KiCad. The schematic uses its adjacent `Project.kicad_sym` and `sym-lib-table`. It documents a panel/harness design, not a PCB layout. The [reading guide](schematic-guide.md) explains the sheet sections and symbols.

## Verification

The Windows runner locates the installed KiCad CLI and Python environment. Override executable locations using `PSU_KICAD_CLI` and `PSU_PYTHON` if needed.

```powershell
.\scripts\run.ps1 verify
.\scripts\run.ps1 calculate
.\scripts\run.ps1 export
.\scripts\run.ps1 open-kicad
```

The normal verification task exports the current schematic and checks ERC, netlist connectivity, calculations and document links. It does not reconstruct the schematic. Results are written to [verification.json](verification.json) and [erc.json](../hardware/erc.json). Reported physical test results remain separate in [testing.md](testing.md).

`python scripts/build_schematic.py` rebuilds the reference drawing from its generator and `hardware/protection-design.json`. This overwrites the generated schematic and library; retain any manual edits before rebuilding. Calculations and verification use Python's standard library. HEIC conversion additionally requires Pillow and pillow-heif.

## Supporting files

All 26 construction images have JPEG copies for repository display. Original images are unchanged; orientation is applied and copied EXIF metadata is omitted from the derivatives. The [manifest](evidence/source-manifest.json) records hashes. The course PDF remains in the excluded local `references/private/` folder and is not included for public redistribution.
