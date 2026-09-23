import asyncio
import ssl
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
from app.core.logging import logger

Base = declarative_base()

# Prepare URL and connection arguments for asyncpg / SQLite
db_url = settings.DATABASE_URL
connect_args = {}

if "postgres" in db_url:
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    # Clean query parameters for asyncpg compatibility with PgBouncer
    if "?" in db_url:
        db_url = db_url.split("?")[0]

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    connect_args = {
        "ssl": ssl_ctx,
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }

USE_ASYNC_ENGINE = True
try:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
        future=True,
        connect_args=connect_args,
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
except (ImportError, Exception) as e:
    logger.warning(f"Async engine creation fell back: {e}")
    USE_ASYNC_ENGINE = False


if not USE_ASYNC_ENGINE:
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")
    if "sqlite" not in sync_url and "postgres" not in sync_url:
        sync_url = "sqlite:///./finguard_local.db"

    sync_engine = create_engine(sync_url, echo=settings.DEBUG, future=True)
    SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

    class AsyncSessionAdapter:
        def __init__(self, sync_session):
            self._session = sync_session

        def add(self, instance):
            self._session.add(instance)

        def add_all(self, instances):
            self._session.add_all(instances)

        async def execute(self, statement, *args, **kwargs):
            return self._session.execute(statement, *args, **kwargs)

        async def flush(self):
            self._session.flush()

        async def commit(self):
            self._session.commit()

        async def rollback(self):
            self._session.rollback()

        async def close(self):
            self._session.close()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
            await self.close()

    def AsyncSessionLocal():
        return AsyncSessionAdapter(SyncSessionLocal())


async def get_db() -> AsyncGenerator:
    if USE_ASYNC_ENGINE:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    else:
        sync_sess = SyncSessionLocal()
        adapter = AsyncSessionAdapter(sync_sess)
        try:
            yield adapter
            await adapter.commit()
        except Exception:
            await adapter.rollback()
            raise
        finally:
            await adapter.close()


async def init_db() -> None:
    try:
        import app.models  # ensure all models are registered on Base.metadata
        if USE_ASYNC_ENGINE:
            async with engine.begin() as conn:
                if "postgres" in db_url:
                    from sqlalchemy import text
                    try:
                        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                    except Exception as ve:
                        logger.warning(f"Vector extension note: {ve}")
                await conn.run_sync(Base.metadata.create_all)
        else:
            Base.metadata.create_all(bind=sync_engine)
        logger.info("Database tables initialized successfully")

        # Ingest knowledge documents into database
        try:
            from rag.ingestion.knowledge_loader import knowledge_loader
            if USE_ASYNC_ENGINE:
                async with AsyncSessionLocal() as session:
                    await knowledge_loader.ingest_all(session)
                    await session.commit()
            else:
                sync_sess = SyncSessionLocal()
                adapter = AsyncSessionAdapter(sync_sess)
                await knowledge_loader.ingest_all(adapter)
                await adapter.commit()
                await adapter.close()
            logger.info("RAG knowledge documents indexed successfully")
        except Exception as ke:
            logger.warning(f"RAG knowledge seeding deferred: {str(ke)}")
    except Exception as e:
        logger.warning(f"Database auto-creation bypassed or failed: {str(e)}")
