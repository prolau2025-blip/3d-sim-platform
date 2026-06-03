import asyncio
import uuid
import os
import tempfile
from gradio_client import Client, handle_file
import shutil

class GSEngine:
    def __init__(self):
        self.generation_queue = {}
        try:
            self.client = Client("ashawkey/LGM")
            print("Connected to HuggingFace LGM Space.")
        except Exception as e:
            print("Failed to connect to LGM:", e)
            self.client = None

    async def start_generation(self, layout_data: dict, image_bytes: bytes = None) -> str:
        job_id = str(uuid.uuid4())
        self.generation_queue[job_id] = {"status": "PENDING"}
        
        if image_bytes is None:
            self.generation_queue[job_id] = {"status": "FAILED", "error": "Image is required for real 3DGS generation."}
            return job_id

        asyncio.create_task(self._real_generate(job_id, image_bytes))
        return job_id

    async def _real_generate(self, job_id: str, image_bytes: bytes):
        self.generation_queue[job_id] = {"status": "GENERATING"}
        try:
            # Save bytes to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(image_bytes)
                tmp_path = tmp.name
                
            if not self.client:
                raise Exception("LGM Client not initialized.")
            
            print(f"[{job_id}] Uploading to HuggingFace LGM API...")
            loop = asyncio.get_event_loop()
            
            def call_api():
                # LGM usually uses /predict as default
                return self.client.predict(
                    handle_file(tmp_path),
                    api_name="/predict"
                )
                
            result = await loop.run_in_executor(None, call_api)
            print(f"[{job_id}] LGM API Output:", result)
            
            if isinstance(result, tuple) and len(result) > 1:
                ply_file = result[1] # Usually index 1 is the PLY, index 0 is video
            elif isinstance(result, str):
                ply_file = result
            else:
                raise Exception("Unexpected output from LGM API: " + str(result))
                
            out_filename = f"{job_id}.ply"
            # Path relative to frontend working directory
            outputs_dir = os.path.join(os.getcwd(), "public", "outputs")
            os.makedirs(outputs_dir, exist_ok=True)
            out_path = os.path.join(outputs_dir, out_filename)
            
            shutil.copy(ply_file, out_path)
            
            self.generation_queue[job_id] = {"status": "READY", "ply_url": f"/outputs/{out_filename}"}
            os.remove(tmp_path)
        except Exception as e:
            print(f"[{job_id}] Generation failed:", e)
            self.generation_queue[job_id] = {"status": "FAILED", "error": str(e)}
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def get_status(self, job_id: str) -> dict:
        return self.generation_queue.get(job_id, {"status": "NOT_FOUND"})

gs_engine_client = GSEngine()
