import google.generativeai as genai
import os
import json

api_key = os.getenv("GEMINI_API_KEY", "MOCK_KEY")
if api_key != "MOCK_KEY":
    genai.configure(api_key=api_key)

class GeminiService:
    def __init__(self):
        self.model_name = 'gemini-1.5-pro'

    async def analyze_spatial_layout(self, text_prompt: str, image_bytes: bytes = None) -> dict:
        if api_key == "MOCK_KEY":
            return {
                "layout": {
                    "primary_object": text_prompt,
                    "lighting": "ambient",
                    "style": "marble",
                    "camera_angle": "front-center",
                    "scale": 1.0
                }
            }
        
        model = genai.GenerativeModel(self.model_name)
        
        prompt = f"""
        Act as a spatial intelligence architect. 
        Analyze the following text prompt and the attached image (if any).
        Output a detailed JSON layout describing the 3D structure, lighting, style, and object placement.
        
        Text Prompt: {text_prompt}
        """
        
        contents = [prompt]
        if image_bytes:
            contents.append({"mime_type": "image/jpeg", "data": image_bytes})
            
        try:
            response = model.generate_content(contents)
            json_start = response.text.find("{")
            json_end = response.text.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                return json.loads(response.text[json_start:json_end])
            return {"raw": response.text}
        except Exception as e:
            return {"error": str(e)}

gemini_client = GeminiService()
