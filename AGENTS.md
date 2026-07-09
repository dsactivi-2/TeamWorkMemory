# AGENTS.md - Shared Memory Server auf Railway

## 1. Projekt-Scope
Diese `AGENTS.md` gilt ausschließlich für den aktuellen Projektordner `/Users/activi/Documents/Dograh & Railway memory` und dessen Unterordner.

Sie definiert nur projektlokale Regeln für dieses Repository. Sie erzeugt keine globalen Regeln und ändert keine Konfiguration außerhalb dieses Projekts.

## 2. Ziel des Projekts
Dieses Projekt beschreibt und steuert ein produktionsnahes Shared-Memory-System für Codex Builder Agents.

Zielarchitektur:
- FastAPI Memory API als zentraler Memory Server
- PostgreSQL als persistenter LangGraph Store
- Redis für Cache und Session State
- Deployment auf Railway

Kritikalität:
- Produktionsnah (Production-Ready), aber nicht voll produktiv im Sinne eines 24/7-Kundeneinsatzes
- Hohe Stabilität und Nachvollziehbarkeit sind erforderlich, da mehrere Builder-Agents darauf aufbauen

## 3. Sprache und Kommunikation
- Kommunikation mit dem User auf Deutsch
- Diese `AGENTS.md` wird auf Deutsch gepflegt
- Technische Begriffe, Dateinamen, Framework-Namen, Befehle und Code-Identifier bleiben unverändert
- Unklare Punkte als offen kennzeichnen, statt Annahmen als Fakten darzustellen
- Aus Dateien oder bestehender Struktur abgeleitete Aussagen immer als erkannt oder abgeleitet behandeln

## 4. Grundarbeitsweise
- Standardablauf für Änderungen: `Discovery -> Zusammenfassung/Plan -> Änderung -> Verify`
- Vor Änderungen immer zuerst den Ist-Zustand ermitteln
- Keine Dateiänderung ohne vorherige kurze Zusammenfassung der geplanten Änderung
- Keine destruktiven Befehle ohne ausdrückliche Freigabe
- Keine Änderungen außerhalb dieses Projekts
- Bei Konflikten, Unsicherheit oder Risiko sofort Rückfrage an Denis oder den Kollegen stellen

## 5. Script-first-Regeln
- Für wiederholbare, umfangreiche oder fehleranfällige Prüfungen gilt `script-first`
- Read-only-Checks dürfen breit automatisiert werden, sofern sie keine produktionsnahen Daten verändern
- Prüfskripte sollen nach Möglichkeit:
  - `set -euo pipefail` verwenden
  - Timestamp-Logs erzeugen
  - einen strukturierten Report mit `PASS`, `WARN`, `FAIL` oder `PASS_WITH_GAPS` liefern
- Schreibende oder deployende Scripts müssen Guardrails enthalten und vorab klar beschreiben, was geändert wird
- Secrets dürfen weder in Logs noch in Reports oder Chat-Ausgaben erscheinen

## 6. Discovery-Regeln
- Vor jeder inhaltlichen Änderung zuerst relevante Dateien und vorhandene Projektstruktur prüfen
- Wenn Projektdateien fehlen, Befehle und Standards als empfohlene Defaults kennzeichnen
- Vor produktionsnahen Änderungen immer zuerst Discovery, dann Draft, dann Dry-Run/Preflight, dann Freigabe, dann Apply/Deploy, dann Post-Check
- Read-only-Checks mit Timestamp sollen nach Möglichkeit vor jeder Schreiboperation laufen, wenn sie sinnvoll zur Risikoreduktion beitragen

## 7. Dateiänderungen
- Standardmäßig nur die minimal nötigen Dateien ändern
- Nie zusätzliche Dateien anlegen oder ändern, wenn es für die aktuelle Aufgabe nicht erforderlich ist
- Keine Secrets, Tokens, API Keys oder private Schlüssel in Dateien schreiben
- Keine harten Kodierungen von Secrets, Tokens oder Service-URLs im Code
- `.env.example` muss beispielhaft und ohne echte Secrets bleiben
- Größere Änderungen an Dokumentation, Architektur oder Schnittstellen müssen konsistent in den zugehörigen Dateien nachgezogen werden

## 8. Umgang mit bestehendem Git-Status
- Bestehende User-Änderungen dürfen nie ungefragt überschrieben oder entfernt werden
- Wenn lokale Änderungen den eigenen Arbeitsbereich berühren, zuerst den Status verstehen und dann vorsichtig integrieren
- Bei Konflikten mit bestehenden Änderungen zuerst zusammenfassen und Freigabe einholen
- Keine History-Rewrites, keine destruktiven Git-Operationen und kein ungefragtes Zurücksetzen von Dateien

## 9. Build, Test, Lint und Format
Bevorzugter Python-Workflow:
- Paketmanager: `uv`
- Test-Framework: `pytest`
- Formatter und Linter: `ruff`
- Dev-Server: FastAPI mit `uvicorn`

Bekannte bzw. festgelegte Standardbefehle:
- Dev-Server: `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- Dependency-Install: `uv sync`
- Fallback-Install: `uv pip install -r requirements.txt`
- Tests: `uv run pytest`
- Erweiterte Tests: `uv run pytest -v --cov`
- Formatierung: `uv run ruff format .`
- Linting mit Auto-Fix: `uv run ruff check --fix .`

Wenn echte Projektdateien später andere Befehle definieren, haben die im Projekt erkannten Befehle Vorrang.

## 10. Sicherheit und Secrets
- Keine Secrets im Code, in Dokumentation, in Logs oder im Chat ausgeben
- Keine echten Zugangsdaten in `README.md`, `AGENTS.md`, `.env.example`, `railway.json` oder vergleichbaren Dateien ablegen
- Environment Variables nur referenzieren, niemals hart einkodieren
- Änderungen an Auth, Token-Verarbeitung, API-Key-Handling oder Secret-Struktur gelten als kritische Änderungen
- Keine Pushes von Secrets in Git

## 11. Deploy-/Produktionsregeln
- Railway ist die primäre produktionsnahe Infrastruktur dieses Projekts
- Keine manuellen Änderungen direkt in der Railway Dashboard UI an produktionsnahen Services oder Datenbanken
- Änderungen sollen bevorzugt über Code, Konfiguration und nachvollziehbare Deploy-Schritte erfolgen
- Deploys nur nach:
  - Discovery
  - Draft/Zusammenfassung
  - lokalem Test oder serverseitigem Dry-Run/Preflight
  - ausdrücklicher Freigabe
  - Deploy
  - Post-Deploy-Check
- Keine Deploys ohne vorherigen lokalen Test
- Neue Services, Änderungen an bestehenden Services oder Änderungen an Railway-Umgebungen nur nach expliziter Freigabe

## 12. Datenbank-, Backup- und Migrationsregeln
- PostgreSQL ist die primäre persistente Datenbank für den LangGraph Store
- Redis ist für Cache und Session State vorgesehen
- Keine automatischen Migrationen ohne explizite Freigabe
- Vor Datenbank-Schreiboperationen oder strukturellen Änderungen Backup-Status prüfen
- Railway-Backups als vorhanden annehmen, aber nie blind vertrauen: vor riskanten Änderungen prüfen, ob ein sinnvoller Restore-Pfad existiert
- Niemals `DROP`, `TRUNCATE` oder direkte destruktive SQL-Manipulationen ohne vorherige Absprache
- Keine manuellen DB-Änderungen ohne Backup-Prüfung

## 13. Kubernetes/Docker/Infra-Regeln
- Aktuelle Infrastruktur: Railway (Web Service + Postgres + Redis)
- Lokale Entwicklung darf `uv` und bei Bedarf Docker nutzen
- Kubernetes, Terraform/OpenTofu, Helm und CI/CD sind in dieser Phase nicht primär und sollen nicht ungefragt eingeführt werden
- Falls solche Infra später hinzukommt, müssen die Regeln projektspezifisch erweitert werden, statt implizit angenommen zu werden

## 14. Logging und Reports
- Read-only-Checks sollen nach Möglichkeit Logs mit Timestamp erzeugen
- Reports sollen möglichst klar als `PASS`, `WARN`, `FAIL` oder `PASS_WITH_GAPS` strukturiert sein
- Logs dürfen keine Secrets enthalten
- Bei produktionsnahen Prüfungen immer festhalten:
  - was geprüft wurde
  - welches Ergebnis vorliegt
  - welche Lücken oder Restrisiken bestehen

## 15. Definition of Done
Eine Aufgabe gilt in diesem Projekt erst als fertig, wenn alle relevanten Punkte erfüllt sind:
- Code ist formatiert
- Linting wurde ausgeführt
- Tests laufen erfolgreich
- Lokaler Test wurde durchgeführt
- Relevante Dokumentation wurde aktualisiert
- Namespace-Konventionen wurden eingehalten
- Keine harten Secrets oder ungesicherten Zugangsdaten wurden eingeführt
- Kritische Änderungen wurden nur nach expliziter Freigabe umgesetzt

## 16. Stop-Kriterien
Sofort stoppen und Rückfrage stellen, wenn:
- Freigabe für Deploy, DB-Änderung, Auth-Änderung oder kritischen Refactor fehlt
- bestehende User-Änderungen betroffen wären
- Namespace-Struktur geändert werden müsste
- unklar ist, ob produktionsnahe Daten überschrieben oder gelöscht würden
- ein Script oder Befehl potenziell destruktiv ist
- Secrets, Tokens oder sensible Konfigurationswerte offengelegt werden könnten

## 17. Projektspezifische Verbote
- Keine direkten Änderungen an Railway-Services oder Datenbanken über die UI
- Keine Experimente im Haupt-Namespace `telesales-builder` ohne klaren Branch oder Test-Namespace
- Kein manuelles Löschen oder Überschreiben bestehender Keys ohne Backup oder Versionierung
- Keine direkten Schreibzugriffe auf produktionsnahe Memory-Daten ohne Namespace- und Key-Struktur
- Keine Änderungen oder Löschungen von Environment Variables ohne Freigabe
- Keine großen Refactorings ohne vorherige Abstimmung
- Kein Ignorieren der bestehenden Namespace-Konventionen

## 18. Bekannte Befehle für dieses Projekt
Diese Befehle sind derzeit als projektweite Standards festgelegt. Solange noch keine echten Projektdateien im Ordner andere Vorgaben definieren, gelten sie als Referenz:

- `uv sync`
- `uv pip install -r requirements.txt`
- `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- `uv run pytest`
- `uv run pytest -v --cov`
- `uv run ruff format .`
- `uv run ruff check --fix .`

## 19. Architekturregeln
- Saubere Layer-Trennung ist Pflicht
- `core/` enthält Konfiguration und zentrale technische Initialisierung
- `api/` enthält Endpoints und API-nahe Logik
- `memory/` enthält Store-Logik
- `schemas/` enthält Pydantic-Modelle oder äquivalente Request/Response-Schemas
- `tests/` enthält automatisierte Tests
- Keine Business-Logik in `main.py`
- Store-Zugriffe nur über `app/memory/store.py` oder das dafür vorgesehene Store-Modul
- Keine direkten DB-Calls außerhalb des Store-Moduls
- Externe Abhängigkeiten zentral und nachvollziehbar anbinden

## 20. Testregeln
Mindesterwartung an Tests:
- Healthcheck Endpoint
- Auth via Bearer und `X-API-Key`
- Namespace-Validation
- `put`, `get` und `search` Endpoints
- Happy Path und Error Cases
- Fehlerfälle wie `401 Unauthorized` und ungültige Requests

Zusätzliche Regeln:
- Tests müssen vor jedem Deploy laufen
- Für kritische Pfade wird mindestens 80 Prozent Coverage angestrebt
- Neue kritische Logik ohne Test gilt nicht als fertig

## 21. Dokumentationsregeln
Pflichtdokumentation für dieses Projekt:
- `README.md`
- `.env.example`
- `CHANGELOG.md`
- `AGENTS.md`

Erwartungen:
- `README.md` enthält Setup-Anleitung, Railway-Hinweise und Dev-Commands
- `.env.example` bleibt aktuell und enthält nur Platzhalter
- `CHANGELOG.md` führt datierte Einträge
- Railway-spezifische Hinweise wie Env Vars, Service-Namen und Healthcheck-URL müssen dokumentiert werden
- Jede größere Änderung muss in mindestens einem relevanten Doku-Artefakt nachvollzogen werden

## 22. Namespace- und Memory-Konventionen
- Primäre Namespace-Konvention: `telesales-builder:*`
- Im Haupt-Namespace dürfen keine ungeplanten Experimente stattfinden
- Wichtige Entscheidungen zu Architektur, Prompting oder Tools sollen nachvollziehbar gespeichert werden
- Schreiben auf bestehende produktionsnahe Memory-Strukturen nur mit klarer Key- und Namespace-Strategie
