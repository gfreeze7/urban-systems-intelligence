$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

Set-Location $ProjectRoot

& $Python -m src.orchestration.pipeline

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

exit 0