from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MemoryStore(ABC):
    @abstractmethod
    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def search(self, namespace: str, query: str | None) -> list[dict[str, Any]]:
        raise NotImplementedError
