$ErrorActionPreference = "Stop"

Write-Host "Initializing Frontend..."
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @react-three/fiber @react-three/drei three lucide-react zustand axios @types/three
cd ..

Write-Host "Initializing Backend..."
mkdir -Force backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn python-multipart pydantic google-generativeai
cd ..

Write-Host "Initialization Complete!"
