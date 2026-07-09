import secrets
from typing import Annotated

from fastapi import Header, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


def verify_api_key(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)] = None,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> str:
    settings = get_settings()
    provided_token = None

    if credentials and credentials.credentials:
        provided_token = credentials.credentials
    elif x_api_key:
        provided_token = x_api_key

    if not provided_token or not secrets.compare_digest(provided_token, settings.memory_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return provided_token
