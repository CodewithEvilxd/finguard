import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

# Standard in-memory SQLite engine
test_sync_engine = create_engine("sqlite:///:memory:", echo=False)
TestingSyncSessionLocal = sessionmaker(bind=test_sync_engine, expire_on_commit=False)


class TestAsyncSessionAdapter:
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


@pytest.fixture(scope="function")
async def db_session():
    Base.metadata.create_all(bind=test_sync_engine)
    sync_sess = TestingSyncSessionLocal()

    # Pre-seed test account for isolated test suite execution
    from app.models.entity import Account
    test_account = Account(
        account_number="ACC-100482",
        account_holder="Apex Global Logistics",
        balance=245000.0,
        currency="USD",
        risk_tier="low",
    )
    sync_sess.add(test_account)

    # Pre-seed test compliance document and chunk for RAG assistant test coverage
    import json
    from app.models.document import Document, DocumentChunk
    from rag.embeddings.embedder import embedder

    test_doc = Document(
        id="doc-test-sop-104",
        title="SOP-104: High Risk Wire Investigation Procedure",
        category="standard_operating_procedure",
        status="active",
        version="v1.0",
    )
    sync_sess.add(test_doc)
    sync_sess.flush()

    content = "SOP-104 Section 2: When an anomalous high-velocity wire transfer is detected, the analyst must verify account activity and halt wire execution."
    vec = embedder.get_embedding(content)
    test_chunk = DocumentChunk(
        document_id=test_doc.id,
        chunk_index=0,
        content=content,
        embedding_json=json.dumps(vec),
    )
    sync_sess.add(test_chunk)
    sync_sess.commit()

    adapter = TestAsyncSessionAdapter(sync_sess)

    yield adapter

    await adapter.close()
    Base.metadata.drop_all(bind=test_sync_engine)


@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
