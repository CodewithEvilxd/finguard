import json
import os
from typing import Any, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentChunk
from rag.chunking.chunker import TextChunker
from rag.embeddings.embedder import embedder
from app.core.logging import logger


class KnowledgeLoader:
    def __init__(self, sources_dir: str = None):
        if sources_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.sources_dir = os.path.join(base_dir, "sources")
        else:
            self.sources_dir = sources_dir
        self.chunker = TextChunker(chunk_size=300, chunk_overlap=30)

    async def ingest_all(self, db: AsyncSession) -> int:
        """
        Scans all Markdown files in backend/rag/sources/, chunks and embeds them,
        and saves them into the database idempotently.
        """
        if not os.path.exists(self.sources_dir):
            logger.warning(f"RAG sources directory not found: {self.sources_dir}")
            return 0

        total_chunks_ingested = 0

        for root, _, files in os.walk(self.sources_dir):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    chunks_added = await self._ingest_file(db, file_path)
                    total_chunks_ingested += chunks_added

        logger.info(f"RAG Knowledge ingestion complete: {total_chunks_ingested} chunks verified/stored.")
        return total_chunks_ingested

    async def _ingest_file(self, db: AsyncSession, file_path: str) -> int:
        rel_path = os.path.relpath(file_path, self.sources_dir)
        category = "general"
        if "policies" in rel_path.lower():
            category = "policy"
        elif "procedures" in rel_path.lower():
            category = "procedure"
        elif "cases" in rel_path.lower():
            category = "case_summary"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from first markdown header
        title = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ")
        for line in content.splitlines():
            line_clean = line.strip()
            if line_clean.startswith("# "):
                title = line_clean[2:].strip()
                break

        # Check if document already exists
        existing_doc = await db.execute(select(Document).where(Document.title == title))
        doc = existing_doc.scalars().first()

        if doc:
            # Document exists; check if it has chunks
            chunks_stmt = select(DocumentChunk).where(DocumentChunk.document_id == doc.id)
            existing_chunks = (await db.execute(chunks_stmt)).scalars().all()
            if len(existing_chunks) > 0:
                return 0
        else:
            doc = Document(
                title=title,
                category=category,
                source_uri=rel_path,
                version="v1.0",
                status="active",
            )
            db.add(doc)
            await db.flush()

        chunks_data = self.chunker.chunk_document(
            text=content,
            metadata={"source_file": rel_path, "category": category, "title": title},
        )

        for chunk in chunks_data:
            chunk_text = chunk["content"]
            vec = embedder.get_embedding(chunk_text)

            chunk_record = DocumentChunk(
                document_id=doc.id,
                chunk_index=chunk["chunk_index"],
                content=chunk_text,
                metadata_json=json.dumps(chunk["metadata"]),
                embedding_json=json.dumps(vec),
            )
            db.add(chunk_record)

        await db.flush()
        return len(chunks_data)


knowledge_loader = KnowledgeLoader()
