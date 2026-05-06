from pydantic import BaseModel, Field
from typing import List, Optional

class MacroBreakdown(BaseModel):
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    fiber_g: Optional[int] = 0

class FoodItem(BaseModel):
    name: str
    quantity: str
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    fiber_g: Optional[int] = 0
    confidence: float = Field(ge=0.0, le=1.0)

class FoodAnalysisResponse(BaseModel):
    foods: List[FoodItem]
    total: MacroBreakdown
    health_score: int = Field(ge=1, le=10)
    suggestions: List[str]
