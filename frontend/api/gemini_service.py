import google.generativeai as genai
import os
import json
import io
from PIL import Image

api_key = os.getenv("GEMINI_API_KEY", "MOCK_KEY")
if api_key != "MOCK_KEY":
    genai.configure(api_key=api_key)

class GeminiService:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'
        self.knowledge_base = ""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            t4bk_path = os.path.join(base_dir, 't4bk.md')
            with open(t4bk_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = f.read()
            print("Successfully loaded historical knowledge base.")
        except Exception as e:
            print("Warning: Could not load t4bk.md knowledge base:", e)

    async def analyze_spatial_layout(self, text_prompt: str, image_bytes: bytes = None) -> dict:
        if api_key == "MOCK_KEY":
            print("WARNING: Gemini API Key not found. Using MOCK data.")
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
        Act as a spatial intelligence architect and historical environment reconstructor.
        You have been provided with the following historical knowledge base from the Malaysian Sejarah curriculum:
        
        === HISTORICAL KNOWLEDGE BASE ===
        {self.knowledge_base}
        =================================
        
        Analyze the following text prompt and the attached image (if any), using the historical knowledge above if relevant.
        Output a detailed JSON layout describing the 3D structure, lighting, style, and object placement for a 3D Gaussian Splat scene.
        Ensure your generated layout reflects historical accuracy where applicable based on the provided textbook context.
        
        Text Prompt: {text_prompt}
        """
        
        contents = [prompt]
        if image_bytes:
            try:
                img = Image.open(io.BytesIO(image_bytes))
                contents.append(img)
            except Exception as e:
                print("Failed to load image with PIL:", e)
            
        try:
            print("Calling Gemini API...")
            response = await model.generate_content_async(contents)
            print("Gemini API Success.")
            json_start = response.text.find("{")
            json_end = response.text.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                return json.loads(response.text[json_start:json_end])
            return {"raw": response.text}
        except Exception as e:
            print("Gemini API Error:", e)
            return {"error": str(e)}

gemini_client = GeminiService()
