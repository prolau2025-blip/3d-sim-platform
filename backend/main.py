from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import gemini_client
from gs_engine import gs_engine_client
import uvicorn
from typing import Optional

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
            
        # 1. AI Reasoning Layer (Gemini)
        layout_data = await gemini_client.analyze_spatial_layout(text_prompt=prompt, image_bytes=image_bytes)
        
        # 2. 3DGS Engine Execution
        job_id = await gs_engine_client.start_generation(layout_data)
        
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
