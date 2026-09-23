from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="policy", nullable=False)  # policy, standard_operating_procedure, regulation, case_summary
    source_uri = Column(String(512), nullable=True)
    version = Column(String(50), default="v1.0", nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active, deprecated

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base, TimestampMixin):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)  # JSON metadata (section, page, tags)
    embedding_json = Column(Text, nullable=True)  # JSON-serialized embedding vector

    document = relationship("Document", back_populates="chunks")

    __table_args__ = (
        Index("idx_chunks_doc_index", "document_id", "chunk_index"),
    )
