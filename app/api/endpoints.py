from fastapi import APIRouter, Depends, Query, status

from app.core.auth import verify_api_key
from app.core.validation import validate_namespace
from app.memory.store import get_store
from app.schemas import (
    MemoryGetResponse,
    MemoryPutRequest,
    MemoryPutResponse,
    MemorySearchResponse,
)

router = APIRouter(
    prefix="/api/v1/memory",
    tags=["memory"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("", response_model=MemoryPutResponse, status_code=status.HTTP_200_OK)
async def put_memory(payload: MemoryPutRequest) -> MemoryPutResponse:
    namespace = validate_namespace(payload.namespace)
    store = get_store()
    store.put(namespace=namespace, key=payload.key, value=payload.value)
    return MemoryPutResponse(status="ok", namespace=namespace, key=payload.key)


@router.get("", response_model=MemoryGetResponse, status_code=status.HTTP_200_OK)
async def get_memory(
    namespace: str = Query(...),
    key: str = Query(...),
) -> MemoryGetResponse:
    valid_namespace = validate_namespace(namespace)
    store = get_store()
    item = store.get(namespace=valid_namespace, key=key)
    return MemoryGetResponse(namespace=valid_namespace, key=key, value=item)


@router.get("/search", response_model=MemorySearchResponse)
async def search_memory(
    namespace: str = Query(...),
    query: str | None = Query(default=None),
) -> MemorySearchResponse:
    valid_namespace = validate_namespace(namespace)
    store = get_store()
    items = store.search(namespace=valid_namespace, query=query)
    return MemorySearchResponse(namespace=valid_namespace, query=query, items=items)
