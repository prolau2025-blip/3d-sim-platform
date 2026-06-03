import asyncio
from gs_engine import gs_engine_client
from gemini_service import gemini_client

async def test():
    print("Testing Gemini Service...")
    res = await gemini_client.analyze_spatial_layout("A beautiful test object")
    print("Gemini Output:", res)
    
    print("Testing GS Engine...")
    job_id = await gs_engine_client.start_generation(res)
    print("Job ID:", job_id)
    
    status = gs_engine_client.get_status(job_id)
    print("Status:", status)
    
    # Wait for completion
    await asyncio.sleep(6)
    status_final = gs_engine_client.get_status(job_id)
    print("Final Status:", status_final)
    print("TEST PASSED")

if __name__ == "__main__":
    asyncio.run(test())
