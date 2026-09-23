from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.db import get_db
from app.schemas.assistant import AssistantQuery, AssistantResponse
from rag.pipeline.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/assistant", tags=["ai-assistant"])


@router.post("/query", response_model=AssistantResponse, status_code=status.HTTP_200_OK)
async def query_investigation_assistant(
    payload: AssistantQuery,
    db: AsyncSession = Depends(get_db),
):
    return await RAGPipeline.process_query(db, payload)
