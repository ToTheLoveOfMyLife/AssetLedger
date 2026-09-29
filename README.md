# AssetLedger

![CI](https://github.com/timwmcqueen/AssetLedger/actions/workflows/ci.yml/badge.svg)

AssetLedger is an API for tracking company computers and other IT equipment from the time they are added until they are retired.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Pydantic
- SQLite for local development
- PostgreSQL-compatible SQLAlchemy configuration through `DATABASE_URL`
- Pytest
- Docker
- GitHub Actions

## Features

- Add and retrieve assets
- Enforce unique asset tags and serial numbers
- Search by tag, serial number, manufacturer, model, or assignee
- Filter by status
- Assign equipment to users and locations
- Mark equipment for repair
- Retire equipment
- Prevent retired equipment from being reassigned
- Keep an event history for each asset
- Health endpoint for deployment checks

## API examples

Create an asset:

```http
POST /api/assets
Content-Type: application/json

{
  "asset_tag": "LT-1042",
  "serial_number": "SN-ABC-1042",
  "manufacturer": "Lenovo",
  "model": "ThinkPad T14",
  "location": "Knoxville Office"
}
```

Assign an asset:

```http
POST /api/assets/1/assign
Content-Type: application/json

{
  "assigned_to": "Jordan Lee",
  "location": "Remote"
}
```

View an asset's history:

```http
GET /api/assets/1/events
```

FastAPI's OpenAPI documentation is available at `/docs` while the service is running.

## Run locally

```bash
python -m venv .venv
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

## Docker

```bash
docker build -t assetledger .
docker run -p 8000:8000 assetledger
```

## Architecture

See [docs/architecture.md](docs/architecture.md).

The route layer handles HTTP requests, the service layer handles asset status rules, SQLAlchemy handles persistence, and Pydantic validates incoming data.

Asset events are stored separately from the current asset record so the API can return both the current state and the history of changes.
