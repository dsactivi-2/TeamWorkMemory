from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MemoryPutRequest(BaseModel):
    namespace: str = Field(min_length=1)
    key: str = Field(min_length=1)
    value: dict[str, Any]


class MemoryPutResponse(BaseModel):
    status: str
    namespace: str
    key: str


class MemoryGetResponse(BaseModel):
    namespace: str
    key: str
    value: dict[str, Any] | None


class SearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    key: str | None = None
    value: dict[str, Any] | None = None


class MemorySearchResponse(BaseModel):
    namespace: str
    query: str | None
    items: list[SearchResult]
