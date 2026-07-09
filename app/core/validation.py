from fastapi import HTTPException, status

from app.core.config import get_settings


def validate_namespace(namespace: str) -> str:
    settings = get_settings()
    if not namespace.startswith(settings.allowed_namespace_prefix):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(f"Namespace must start with '{settings.allowed_namespace_prefix}'."),
        )
    return namespace
