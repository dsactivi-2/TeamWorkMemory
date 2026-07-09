import pytest
from fastapi.testclient import TestClient

from app.core.config import clear_settings_cache
from app.memory.store import reset_store


@pytest.fixture(autouse=True)
def reset_app_state(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEMORY_API_KEY", "test-api-key")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("ALLOW_INMEMORY_STORE", "true")
    clear_settings_cache()
    reset_store()
    yield
    clear_settings_cache()
    reset_store()


@pytest.fixture()
def client() -> TestClient:
    from app.main import app

    return TestClient(app)


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-api-key"}
