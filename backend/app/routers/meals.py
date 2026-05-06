from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.meal import MealCreate, MealResponse
from app.repositories.meal_repo import MealRepository
from app.dependencies import get_current_user, get_db
from google.cloud import firestore

router = APIRouter(prefix="/meals", tags=["Meals"])

def get_meal_repo(db: firestore.AsyncClient = Depends(get_db)) -> MealRepository:
    return MealRepository(db)

@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal: MealCreate,
    user: dict = Depends(get_current_user),
    repo: MealRepository = Depends(get_meal_repo)
):
    try:
        return await repo.create_meal(user["sub"], meal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[MealResponse])
async def get_meals(
    user: dict = Depends(get_current_user),
    repo: MealRepository = Depends(get_meal_repo)
):
    try:
        return await repo.get_meals(user["sub"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
