# AssetLedger

![CI](https://github.com/ToTheLoveOfMyLife/InheritanceOOP/actions/workflows/ci.yml/badge.svg)

A production-style **IT asset lifecycle API** built with Python, FastAPI, SQLAlchemy, and automated tests.

This project replaces an early Java OOP coursework repository with a substantially more realistic application while preserving the original coursework under `legacy/`.

## Why this project

IT teams need more than a spreadsheet to know who has a device, whether it is available, in repair, or retired, and how its state changed over time. AssetLedger models that lifecycle as an API with durable records and an audit trail.

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

- Create and retrieve managed assets
- Unique asset-tag and serial-number enforcement
- Search by tag, serial, manufacturer, model, or assignee
- Filter inventory by lifecycle state
- Assign assets to users and locations
- Mark devices for repair
- Retire assets and prevent invalid reassignment
- Durable audit history for lifecycle events
- Structured problem responses for conflicts/not-found cases
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

View the audit trail:

```http
GET /api/assets/1/events
```

Interactive OpenAPI documentation is available at `/docs` when the service is running.

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

See [docs/architecture.md](docs/architecture.md) for the request flow and layer boundaries.

## Engineering decisions

The HTTP layer delegates lifecycle rules to a service module instead of embedding them in route handlers. SQLAlchemy models own persistence, Pydantic models validate the external contract, and asset events provide an append-only audit history.

The test suite exercises the API across complete lifecycle transitions rather than only checking isolated helper functions.

## Portfolio history

The repository's original Java inheritance exercise is retained under `legacy/` to document progression from coursework into application engineering.
