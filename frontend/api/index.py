import os

# Load local .env file if it exists (for local testing without python-dotenv)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                try:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                except ValueError:
                    pass

from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
import httpx
import urllib.parse

try:
    from api.gemini_service import gemini_client
    from api.gs_engine import gs_engine_client
except ImportError:
    from gemini_service import gemini_client
    from gs_engine import gs_engine_client

app = FastAPI(title="3DGS Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationResponse(BaseModel):
    job_id: str
    status: str

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_3d_world(
    prompt: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    try:
        image_bytes = None
        if image:
            image_bytes = await image.read()
        else:
            # Fallback to a free Text-to-Image API if no image is uploaded
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
            async with httpx.AsyncClient() as client:
                resp = await client.get(image_url, timeout=30.0)
                if resp.status_code == 200:
                    image_bytes = resp.content
            
        layout_data = await gemini_client.analyze_spatial_layout(text_prompt=prompt, image_bytes=image_bytes)
        job_id = await gs_engine_client.start_generation(layout_data, prompt=prompt, image_bytes=image_bytes)
        
        return GenerationResponse(job_id=job_id, status="PENDING")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    status_data = gs_engine_client.get_status(job_id)
    if status_data["status"] == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Job not found")
    return status_data

if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
