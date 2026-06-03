$ErrorActionPreference = "Stop"
mkdir -Force backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn python-multipart pydantic google-generativeai
