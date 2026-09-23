import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import logger
from app.api.routes.health import router as health_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.investigations import router as investigations_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting FinGuard AI Backend service in [{settings.ENVIRONMENT}] environment")
    await init_db()
    yield
    logger.info("FinGuard AI Backend service shutdown complete")


app = FastAPI(
    title="FinGuard AI Core API",
    version="1.0.0",
    description="Explainable Financial Fraud and Anomaly Intelligence Platform API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID Middleware
@app.middleware("http")
async def request_id_and_timing_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    if request.url.path not in {"/api/v1/health", "/api/v1/ready"}:
        logger.info(
            f"{request.method} {request.url.path} completed with {response.status_code} in {process_time:.4f}s",
            extra={"request_id": request_id},
        )
    return response


# Standard Error Envelopes
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = request.headers.get("X-Request-ID")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Request payload failed validation schema checks.",
            "request_id": request_id,
            "details": {"errors": exc.errors()},
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    request_id = request.headers.get("X-Request-ID")
    logger.error(f"Unhandled exception during {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal system error occurred. Please reference the request ID for assistance.",
            "request_id": request_id,
            "details": None,
        },
    )


# API Version 1 Routers
api_v1_prefix = "/api/v1"
app.include_router(health_router, prefix=api_v1_prefix)
app.include_router(transactions_router, prefix=api_v1_prefix)
app.include_router(alerts_router, prefix=api_v1_prefix)
app.include_router(investigations_router, prefix=api_v1_prefix)
app.include_router(accounts_router, prefix=api_v1_prefix)
app.include_router(assistant_router, prefix=api_v1_prefix)
app.include_router(analytics_router, prefix=api_v1_prefix)


@app.get("/", tags=["root"])
async def root():
    return {
        "service": "FinGuard AI Core API",
        "version": "1.0.0",
        "api_docs": "/docs",
        "health": "/api/v1/health",
        "environment": settings.ENVIRONMENT,
    }
