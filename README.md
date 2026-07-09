# memory-server

Shared Memory Server für Codex Builder Agents auf Railway.

## Ziel

Dieses Projekt stellt eine FastAPI-basierte Memory API bereit. Der produktionsnahe Zielbetrieb nutzt:

- Railway als Plattform
- PostgreSQL als persistenten LangGraph Store
- Redis für Cache und Session State

Für lokale Entwicklung und Tests kann ohne `DATABASE_URL` ein In-Memory-Store verwendet werden.

## Projektstruktur

```text
app/
  core/
  api/
  memory/
tests/
main.py
```

## Voraussetzungen

- Python 3.11+
- `uv`

## Lokales Setup

1. Abhängigkeiten installieren:

```bash
uv sync
```

2. Beispiel-Umgebung kopieren und lokal befüllen:

```bash
cp .env.example .env
```

3. Dev-Server starten:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests und Qualität

```bash
uv run pytest
uv run pytest -v --cov
uv run ruff format .
uv run ruff check --fix .
```

## API-Überblick

### Healthcheck

- `GET /health`

### Memory API

Alle Endpoints verlangen Bearer-Auth oder `X-API-Key`.

- `POST /api/v1/memory`
- `GET /api/v1/memory`
- `GET /api/v1/memory/search`

### Beispiel `POST /api/v1/memory`

```json
{
  "namespace": "telesales-builder:decisions",
  "key": "architecture",
  "value": {
    "store": "postgres",
    "cache": "redis"
  }
}
```

## Namespace-Regel

Nur Namespaces mit Präfix `telesales-builder:` sind gültig.

## Railway-Hinweise

- Service-Typ: Web Service
- Start Command: `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`
- Benötigte Env Vars:
  - `MEMORY_API_KEY`
  - `DATABASE_URL`
  - `REDIS_URL`
  - `ALLOWED_NAMESPACE_PREFIX`
- Healthcheck-URL: `/health`

## GitHub Automation

Das Projekt enthält zwei GitHub-Actions-Workflows:

- `CI`: läuft auf Push und Pull Request und führt `uv sync`, `ruff` und `pytest` aus
- `Deploy to Railway`: läuft manuell oder auf Push nach `main`, führt erst die Quality Gates aus und deployed danach mit der Railway CLI

Für den Deploy-Workflow werden folgende GitHub Secrets erwartet:

- `RAILWAY_TOKEN`

Feste Deploy-Zielwerte in diesem Projekt:

- Railway Service Name: `DograhTeamMem`
- Railway Environment Name: `production`
- Railway Environment ID: wird von Railway automatisch vergeben und kann nicht frei gewählt werden

Empfohlen für Railway:

- GitHub-Repository mit dem Railway-Service verknüpfen
- in Railway `Wait for CI` aktivieren, damit Deploys erst nach erfolgreicher GitHub-CI starten
- nur `main` als produktionsnahen Deploy-Branch verwenden

## Wichtige Sicherheitsregeln

- Keine echten Secrets in Git
- Keine Railway-UI-Änderungen an produktionsnahen Services ohne Freigabe
- Keine destruktiven SQL-Befehle
- Deploys nur nach lokalem Test und expliziter Freigabe
