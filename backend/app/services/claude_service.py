import anthropic
from app.config import get_settings
from typing import AsyncGenerator

MEAL_PLANNER_SYSTEM = """
You are NutriSense AI's nutrition engine. Generate a 7-day personalized meal plan.
Return ONLY valid JSON with this structure:
{
  "week": [{
    "day": "Monday",
    "meals": {
      "breakfast": {"name": str, "calories": int, "protein_g": int, "carbs_g": int, "fat_g": int, "prep_minutes": int, "ingredients": [str], "instructions": str},
      "lunch": {...},
      "dinner": {...},
      "snacks": [{"name": str, "calories": int}]
    },
    "total_calories": int,
    "meal_prep_tips": [str]
  }]
}
"""

HABIT_COACH_SYSTEM = """
You are a compassionate nutrition coach. Analyze 7-day eating history.
Return ONLY valid JSON:
{
  "positives": [{"habit": str, "reason": str}],
  "improvements": [{"area": str, "tip": str, "difficulty": "easy|medium|hard"}],
  "micro_habit": {"title": str, "description": str, "why_it_works": str},
  "message": str,
  "score": number (1-100)
}
"""

class ClaudeService:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_meal_plan_stream(self, user_goals: str) -> AsyncGenerator[str, None]:
        stream = await self.client.messages.create(
            max_tokens=4000,
            system=MEAL_PLANNER_SYSTEM,
            messages=[
                {"role": "user", "content": f"Generate a meal plan based on these goals: {user_goals}"}
            ],
            model="claude-3-opus-20240229",
            stream=True
        )
        
        async for event in stream:
            if event.type == "text_delta":
                yield event.text

    async def get_habit_insights(self, history: str) -> str:
        response = await self.client.messages.create(
            max_tokens=2000,
            system=HABIT_COACH_SYSTEM,
            messages=[
                {"role": "user", "content": f"Analyze this eating history: {history}"}
            ],
            model="claude-3-sonnet-20240229",
        )
        return response.content[0].text
