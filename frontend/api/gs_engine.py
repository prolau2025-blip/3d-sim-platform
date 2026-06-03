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

    async def start_generation(self, layout_data: dict, prompt: str = "", image_bytes: bytes = None) -> str:
        job_id = str(uuid.uuid4())
        self.generation_queue[job_id] = {"status": "PENDING"}
        
        if image_bytes is None:
            self.generation_queue[job_id] = {"status": "FAILED", "error": "Image is required for 3DGS generation (Fallback failed)."}
            return job_id

        asyncio.create_task(self._real_generate(job_id, prompt, image_bytes))
        return job_id

    async def _real_generate(self, job_id: str, prompt: str, image_bytes: bytes = None):
        self.generation_queue[job_id] = {"status": "GENERATING"}
        tmp_path = None
        try:
            if image_bytes:
                # Save bytes to a temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    tmp.write(image_bytes)
                    tmp_path = tmp.name
                    
            if not self.client:
                raise Exception("LGM Client not initialized.")
            
            print(f"[{job_id}] Uploading to HuggingFace LGM API...")
            loop = asyncio.get_event_loop()
            
            def call_api():
                # LGM takes 6 parameters for /process: image, prompt, negative_prompt, elevation, steps, seed
                return self.client.predict(
                    handle_file(tmp_path), # input_image
                    prompt, # input_text
                    "ugly, blurry, lowres", # input_neg_text
                    0, # input_elevation
                    30, # input_num_steps
                    42, # input_seed
                    api_name="/process"
                )
                
            result = await loop.run_in_executor(None, call_api)
            print(f"[{job_id}] LGM API Output:", result)
            
            # The result is a tuple: (multi_view_image, output_video_path, output_ply_path)
            if isinstance(result, tuple) and len(result) > 2:
                ply_file = result[2] 
            elif isinstance(result, tuple) and len(result) > 1:
                ply_file = result[-1]
            elif isinstance(result, str):
                ply_file = result
            else:
                raise Exception("Unexpected output from LGM API: " + str(result))
                
            out_filename = f"{job_id}.ply"
            outputs_dir = os.path.join(os.getcwd(), "public", "outputs")
            os.makedirs(outputs_dir, exist_ok=True)
            out_path = os.path.join(outputs_dir, out_filename)
            
            shutil.copy(ply_file, out_path)
            
            self.generation_queue[job_id] = {"status": "READY", "ply_url": f"/outputs/{out_filename}"}
        except Exception as e:
            print(f"[{job_id}] Generation failed:", e)
            self.generation_queue[job_id] = {"status": "FAILED", "error": str(e)}
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def get_status(self, job_id: str) -> dict:
        return self.generation_queue.get(job_id, {"status": "NOT_FOUND"})

gs_engine_client = GSEngine()
