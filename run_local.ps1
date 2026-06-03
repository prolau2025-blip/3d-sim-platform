$ErrorActionPreference = "Stop"
$baseDir = "C:\Users\SJKCWUTECKPERANTIFAS\.gemini\antigravity\scratch\3d_sim_project"
cd $baseDir

$nodeDir = (Get-ChildItem -Path "node_extracted" -Directory)[0].FullName
$env:PATH = "$nodeDir;" + $env:PATH

cd frontend

Write-Host "Starting FastAPI Backend on port 8000..."
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "api.index:app", "--host", "127.0.0.1", "--port", "8000"

Write-Host "Starting Vite Frontend..."
npm run dev
