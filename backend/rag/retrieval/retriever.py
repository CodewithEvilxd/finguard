import json
from typing import List, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentChunk
from rag.embeddings.embedder import embedder


class KnowledgeRetriever:
    @staticmethod
    async def retrieve_relevant_chunks(
        db: AsyncSession,
        query: str,
        top_k: int = 3,
        min_similarity: float = 0.0,
    ) -> List[Tuple[DocumentChunk, Document, float]]:
        query_vector = embedder.get_embedding(query)

        # Retrieve all active chunks
        stmt = (
            select(DocumentChunk, Document)
            .join(Document, DocumentChunk.document_id == Document.id)
            .where(Document.status == "active")
        )
        result = await db.execute(stmt)
        rows = result.all()

        scored_results = []
        for chunk, doc in rows:
            if chunk.embedding_json:
                chunk_vec = json.loads(chunk.embedding_json)
                sim = embedder.cosine_similarity(query_vector, chunk_vec)
                if sim >= min_similarity:
                    scored_results.append((chunk, doc, sim))

        # Sort by similarity descending
        scored_results.sort(key=lambda x: x[2], reverse=True)
        return scored_results[:top_k]
