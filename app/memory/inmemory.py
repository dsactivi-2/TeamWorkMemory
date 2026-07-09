from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.memory.base import MemoryStore


class InMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._data: dict[str, dict[str, dict[str, Any]]] = {}

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        bucket = self._data.setdefault(namespace, {})
        bucket[key] = deepcopy(value)

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        value = self._data.get(namespace, {}).get(key)
        return deepcopy(value) if value is not None else None

    def search(self, namespace: str, query: str | None) -> list[dict[str, Any]]:
        bucket = self._data.get(namespace, {})
        results: list[dict[str, Any]] = []
        lowered_query = query.lower() if query else None

        for key, value in bucket.items():
            haystack = f"{key} {value}".lower()
            if lowered_query and lowered_query not in haystack:
                continue
            results.append({"key": key, "value": deepcopy(value)})

        return results
