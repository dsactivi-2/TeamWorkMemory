from __future__ import annotations

from typing import Any

from app.core.config import get_settings
from app.memory.base import MemoryStore
from app.memory.inmemory import InMemoryStore

_STORE: MemoryStore | None = None


class LangGraphPostgresStoreAdapter(MemoryStore):
    def __init__(self, backend: Any) -> None:
        self.backend = backend

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        self.backend.put((namespace,), key, value)

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        result = self.backend.get((namespace,), key)
        if result is None:
            return None
        if isinstance(result, dict):
            return result
        if hasattr(result, "value"):
            return result.value
        return {"result": result}

    def search(self, namespace: str, query: str | None) -> list[dict[str, Any]]:
        results = self.backend.search((namespace,), query=query)
        normalized: list[dict[str, Any]] = []
        for item in results:
            if isinstance(item, dict):
                normalized.append(item)
                continue
            normalized.append(
                {
                    "key": getattr(item, "key", None),
                    "value": getattr(item, "value", None),
                }
            )
        return normalized


def _build_store() -> MemoryStore:
    settings = get_settings()

    if settings.database_url:
        try:
            from langgraph.store.postgres import PostgresStore
        except ImportError as exc:
            raise RuntimeError(
                "DATABASE_URL is set, but langgraph Postgres support is unavailable."
            ) from exc

        backend = PostgresStore.from_conn_string(settings.database_url)
        return LangGraphPostgresStoreAdapter(backend=backend)

    if settings.allow_inmemory_store:
        return InMemoryStore()

    raise RuntimeError(
        "No store backend configured. Set DATABASE_URL or allow the in-memory store."
    )


def initialize_store() -> MemoryStore:
    global _STORE
    if _STORE is None:
        _STORE = _build_store()
    return _STORE


def get_store() -> MemoryStore:
    return initialize_store()


def reset_store() -> None:
    global _STORE
    _STORE = None
