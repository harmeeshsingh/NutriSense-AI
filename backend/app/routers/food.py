from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.services.gemini_service import GeminiService
from app.models.nutrition import FoodAnalysisResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/food", tags=["Food"])

@router.post("/analyze", response_model=FoodAnalysisResponse)
async def analyze_food(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    gemini_service: GeminiService = Depends(GeminiService)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided is not an image."
        )
        
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 10MB limit."
        )
        
    try:
        result = await gemini_service.analyze_food_image(contents, file.content_type)
        return FoodAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        )
