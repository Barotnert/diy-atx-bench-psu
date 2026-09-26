param([ValidateSet('verify','calculate','export','rebuild','open-kicad')][string]$Action = 'verify')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath = $env:PSU_PYTHON
if (-not $pythonPath) {
    $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) { $pythonPath = $bundledPython }
    else { $pythonPath = (Get-Command python -ErrorAction Stop).Source }
}
$kicadPath = $env:PSU_KICAD_CLI
if (-not $kicadPath) {
    $kicadPath = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
    if (-not (Test-Path -LiteralPath $kicadPath)) { $kicadPath = (Get-Command kicad-cli -ErrorAction Stop).Source }
}
function Invoke-Checked([string]$Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Command failed with exit code $LASTEXITCODE" }
}
if ($Action -eq 'open-kicad') {
    $editorPath = Join-Path (Split-Path -Parent $kicadPath) 'eeschema.exe'
    Start-Process -FilePath $editorPath -ArgumentList ('"' + (Join-Path $projectRoot 'hardware\diy_atx_psu.kicad_sch') + '"')
    exit 0
}
if ($Action -in @('calculate','rebuild','verify')) { Invoke-Checked $pythonPath @('-X','utf8','scripts/calculate.py') }
if ($Action -eq 'rebuild') { Invoke-Checked $pythonPath @('-X','utf8','scripts/build_schematic.py') }
if ($Action -in @('export','rebuild','verify')) {
    Invoke-Checked $kicadPath @('sch','erc','--format','json','--exit-code-violations','-o','hardware/erc.json','hardware/diy_atx_psu.kicad_sch')
    Invoke-Checked $kicadPath @('sch','export','netlist','--format','kicadxml','-o','hardware/diy_atx_psu.net','hardware/diy_atx_psu.kicad_sch')
    Invoke-Checked $kicadPath @('sch','export','svg','-o','docs/images/schematic/','hardware/diy_atx_psu.kicad_sch')
    $svgPath = Join-Path $projectRoot 'docs/images/schematic/diy_atx_psu.svg'
    $svgLines = [System.IO.File]::ReadAllLines($svgPath) | ForEach-Object { $_.TrimEnd() }
    [System.IO.File]::WriteAllText($svgPath, (($svgLines -join "`n") + "`n"), [System.Text.UTF8Encoding]::new($false))
}
if ($Action -in @('verify','rebuild')) { Invoke-Checked $pythonPath @('-X','utf8','scripts/verify_project.py') }
