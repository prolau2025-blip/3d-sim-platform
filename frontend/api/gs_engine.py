import asyncio
import uuid

class GSEngine:
    def __init__(self):
        self.generation_queue = {}

    async def start_generation(self, layout_data: dict, original_image_url: str = None) -> str:
        job_id = str(uuid.uuid4())
        self.generation_queue[job_id] = "PENDING"
        asyncio.create_task(self._mock_generate(job_id))
        return job_id

    async def _mock_generate(self, job_id: str):
        self.generation_queue[job_id] = "GENERATING"
        await asyncio.sleep(5)
        self.generation_queue[job_id] = "READY"
        
    def get_status(self, job_id: str) -> dict:
        status = self.generation_queue.get(job_id, "NOT_FOUND")
        response = {"status": status}
        if status == "READY":
            # Using locally hosted fast splat file
            response["ply_url"] = "/bonsai.splat"
        return response

gs_engine_client = GSEngine()
