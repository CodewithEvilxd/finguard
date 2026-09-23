from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "service": "finguard-backend",
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check(db: AsyncSession = Depends(get_db)):
    # Verify database connection
    try:
        await db.execute(text("SELECT 1"))
        db_ready = True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection unavailable: {str(e)}",
        )

    return {
        "status": "ready",
        "service": "finguard-backend",
        "database": "connected" if db_ready else "error",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
