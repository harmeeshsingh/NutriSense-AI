from google.cloud.firestore_v1.async_client import AsyncClient
from google.cloud.firestore_v1.base_query import FieldFilter
from app.models.meal import MealCreate, MealResponse
from typing import List
from datetime import datetime

class MealRepository:
    def __init__(self, db: AsyncClient):
        self.db = db

    def _get_collection(self, user_id: str):
        return self.db.collection("users").document(user_id).collection("meals")

    async def create_meal(self, user_id: str, meal: MealCreate) -> MealResponse:
        collection = self._get_collection(user_id)
        meal_dict = meal.model_dump()
        
        # Datetime serialization for Firestore
        meal_dict["timestamp"] = meal.timestamp

        doc_ref = collection.document()
        await doc_ref.set(meal_dict)

        return MealResponse(
            id=doc_ref.id,
            user_id=user_id,
            **meal_dict
        )

    async def get_meals(self, user_id: str, date: datetime = None) -> List[MealResponse]:
        collection = self._get_collection(user_id)
        
        # Simple fetch, can add date filtering later
        docs = collection.stream()
        
        meals = []
        async for doc in docs:
            data = doc.to_dict()
            meals.append(MealResponse(id=doc.id, user_id=user_id, **data))
            
        return meals
