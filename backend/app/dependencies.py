import redis.asyncio as redis
from google.cloud import firestore
from fastapi import Request, Depends, HTTPException, status
from app.config import get_settings, Settings
from typing import AsyncGenerator

# Firestore instance (lazy initialization)
_db = None

def get_db(settings: Settings = Depends(get_settings)) -> firestore.AsyncClient:
    global _db
    if _db is None:
        _db = firestore.AsyncClient(project=settings.GCP_PROJECT_ID)
    return _db

async def get_redis(settings: Settings = Depends(get_settings)) -> AsyncGenerator[redis.Redis, None]:
    client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()

def get_current_user(request: Request) -> dict:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user
