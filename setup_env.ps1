$ErrorActionPreference = "Stop"
$baseDir = "C:\Users\SJKCWUTECKPERANTIFAS\.gemini\antigravity\scratch\3d_sim_project"
cd $baseDir

if (-not (Test-Path "node_extracted")) {
    $nodeVersion = "v20.12.2"
    $zipUrl = "https://nodejs.org/dist/$nodeVersion/node-$nodeVersion-win-x64.zip"
    $zipPath = "node.zip"
    $extractPath = "node_extracted"

    Write-Host "Downloading Node.js..."
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

    Write-Host "Extracting Node.js..."
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
}

$nodeDir = (Get-ChildItem -Path "node_extracted" -Directory)[0].FullName
$env:PATH = "$nodeDir;" + $env:PATH

cd frontend
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python venv..."
    python -m venv venv
}

Write-Host "Installing Python dependencies..."
.\venv\Scripts\pip install -r requirements.txt

Write-Host "Installing npm dependencies..."
npm install

Write-Host "Setup Complete!"
