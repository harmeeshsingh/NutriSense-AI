from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.services.claude_service import ClaudeService
from app.dependencies import get_current_user

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.post("/generate")
async def generate_planner(
    goals: str,
    user: dict = Depends(get_current_user),
    claude_service: ClaudeService = Depends(ClaudeService)
):
    async def event_generator():
        try:
            async for chunk in claude_service.generate_meal_plan_stream(goals):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/coach/insights")
async def get_insights(
    history: str,
    user: dict = Depends(get_current_user),
    claude_service: ClaudeService = Depends(ClaudeService)
):
    try:
        result = await claude_service.get_habit_insights(history)
        return {"insights": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
