import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from tenacity import retry, stop_after_attempt, wait_exponential
import json
from app.config import get_settings

FOOD_ANALYSIS_PROMPT = """
Analyze this food image. Return ONLY valid JSON — no markdown, no explanation:
{
  "foods": [{
    "name": "string",
    "quantity": "string (e.g. 1 cup, 200g)",
    "calories": number,
    "protein_g": number,
    "carbs_g": number,
    "fat_g": number,
    "fiber_g": number,
    "confidence": number (0.0-1.0)
  }],
  "total": {"calories": number, "protein_g": number, "carbs_g": number, "fat_g": number},
  "health_score": number (1-10),
  "suggestions": ["string"]
}
"""

class GeminiService:
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-pro")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def analyze_food_image(self, image_data: bytes, mime_type: str) -> dict:
        try:
            # Create a blob for the image
            vision_content = [
                {"mime_type": mime_type, "data": image_data},
                FOOD_ANALYSIS_PROMPT
            ]
            
            response = await self.model.generate_content_async(vision_content)
            # Parse the JSON response
            text_response = response.text
            # Simple cleanup in case it returned markdown block
            if text_response.startswith("```json"):
                text_response = text_response[7:-3].strip()
            elif text_response.startswith("```"):
                text_response = text_response[3:-3].strip()
            
            return json.loads(text_response)
        except GoogleAPIError as e:
            raise e
        except json.JSONDecodeError:
            raise ValueError("Failed to parse Gemini response as JSON")
