from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.nutrition import MacroBreakdown, FoodItem

class MealBase(BaseModel):
    name: str
    type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    timestamp: datetime
    foods: List[FoodItem]
    total_macros: MacroBreakdown

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    id: str
    user_id: str
