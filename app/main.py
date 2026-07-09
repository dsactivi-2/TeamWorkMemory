from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router as memory_router
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.memory.store import initialize_store


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    initialize_store()
    yield


app = FastAPI(
    title="Telesales Shared Memory Server",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(memory_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "memory-server",
    }
