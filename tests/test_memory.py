from app.core.config import clear_settings_cache
from app.memory.inmemory import InMemoryStore
from app.memory.store import get_store, reset_store


def test_healthcheck(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_requires_auth_for_put(client):
    response = client.post(
        "/api/v1/memory",
        json={
            "namespace": "telesales-builder:decisions",
            "key": "architecture",
            "value": {"choice": "postgres"},
        },
    )

    assert response.status_code == 401


def test_accepts_bearer_auth(client, auth_headers):
    response = client.post(
        "/api/v1/memory",
        headers=auth_headers,
        json={
            "namespace": "telesales-builder:decisions",
            "key": "architecture",
            "value": {"choice": "postgres"},
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_accepts_x_api_key_auth(client):
    response = client.post(
        "/api/v1/memory",
        headers={"X-API-Key": "test-api-key"},
        json={
            "namespace": "telesales-builder:decisions",
            "key": "tooling",
            "value": {"package_manager": "uv"},
        },
    )

    assert response.status_code == 200


def test_rejects_invalid_namespace(client, auth_headers):
    response = client.post(
        "/api/v1/memory",
        headers=auth_headers,
        json={
            "namespace": "invalid:decisions",
            "key": "architecture",
            "value": {"choice": "postgres"},
        },
    )

    assert response.status_code == 422
    assert "Namespace must start with" in response.json()["detail"]


def test_put_get_and_search_flow(client, auth_headers):
    put_response = client.post(
        "/api/v1/memory",
        headers=auth_headers,
        json={
            "namespace": "telesales-builder:decisions",
            "key": "auth",
            "value": {"strategy": "bearer_or_x_api_key"},
        },
    )
    assert put_response.status_code == 200

    get_response = client.get(
        "/api/v1/memory",
        headers=auth_headers,
        params={"namespace": "telesales-builder:decisions", "key": "auth"},
    )
    assert get_response.status_code == 200
    assert get_response.json()["value"]["strategy"] == "bearer_or_x_api_key"

    search_response = client.get(
        "/api/v1/memory/search",
        headers=auth_headers,
        params={"namespace": "telesales-builder:decisions", "query": "bearer"},
    )
    assert search_response.status_code == 200
    assert len(search_response.json()["items"]) == 1


def test_invalid_request_returns_422(client, auth_headers):
    response = client.post(
        "/api/v1/memory",
        headers=auth_headers,
        json={
            "namespace": "telesales-builder:decisions",
            "key": "",
            "value": {"strategy": "invalid"},
        },
    )

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_store_uses_inmemory_backend_without_database(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("ALLOW_INMEMORY_STORE", "true")
    clear_settings_cache()
    reset_store()

    store = get_store()

    assert isinstance(store, InMemoryStore)


def test_store_raises_when_no_backend_is_configured(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("ALLOW_INMEMORY_STORE", "false")
    clear_settings_cache()
    reset_store()

    try:
        get_store()
    except RuntimeError as exc:
        assert "No store backend configured" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError when no backend is configured.")
