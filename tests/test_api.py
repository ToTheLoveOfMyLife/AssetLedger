import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from fastapi.testclient import TestClient
import pytest

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def new_asset_payload():
    return {
        "asset_tag": "LT-1042",
        "serial_number": "SN-ABC-1042",
        "manufacturer": "Lenovo",
        "model": "ThinkPad T14",
        "location": "Knoxville Office",
    }


def test_asset_lifecycle_and_audit_history(client: TestClient):
    created = client.post("/api/assets", json=new_asset_payload())
    assert created.status_code == 201
    asset_id = created.json()["id"]
    assert created.json()["status"] == "AVAILABLE"

    assigned = client.post(
        f"/api/assets/{asset_id}/assign",
        json={"assigned_to": "Jordan Lee", "location": "Remote"},
    )
    assert assigned.status_code == 200
    assert assigned.json()["status"] == "ASSIGNED"
    assert assigned.json()["assigned_to"] == "Jordan Lee"

    repaired = client.post(
        f"/api/assets/{asset_id}/repair",
        json={"details": "Battery health is below replacement threshold."},
    )
    assert repaired.status_code == 200
    assert repaired.json()["status"] == "REPAIR"

    retired = client.post(f"/api/assets/{asset_id}/retire")
    assert retired.status_code == 200
    assert retired.json()["status"] == "RETIRED"
    assert retired.json()["assigned_to"] is None

    events = client.get(f"/api/assets/{asset_id}/events")
    assert events.status_code == 200
    assert [event["event_type"] for event in events.json()] == [
        "CREATED",
        "ASSIGNED",
        "REPAIR",
        "RETIRED",
    ]


def test_rejects_duplicate_asset_identifiers(client: TestClient):
    assert client.post("/api/assets", json=new_asset_payload()).status_code == 201
    duplicate = client.post("/api/assets", json=new_asset_payload())
    assert duplicate.status_code == 409
    assert duplicate.json()["title"] == "Duplicate asset"


def test_retired_asset_cannot_be_reassigned(client: TestClient):
    created = client.post("/api/assets", json=new_asset_payload()).json()
    asset_id = created["id"]
    client.post(f"/api/assets/{asset_id}/retire")

    response = client.post(
        f"/api/assets/{asset_id}/assign",
        json={"assigned_to": "Taylor Morgan", "location": "Lexington"},
    )

    assert response.status_code == 409
    assert "Retired assets" in response.json()["detail"]


def test_search_and_status_filter(client: TestClient):
    client.post("/api/assets", json=new_asset_payload())
    second = new_asset_payload() | {
        "asset_tag": "DT-2001",
        "serial_number": "SN-DESK-2001",
        "manufacturer": "Dell",
        "model": "OptiPlex 7020",
    }
    client.post("/api/assets", json=second)

    search = client.get("/api/assets?search=ThinkPad")
    assert search.status_code == 200
    assert len(search.json()) == 1
    assert search.json()[0]["asset_tag"] == "LT-1042"

    available = client.get("/api/assets?status=AVAILABLE")
    assert available.status_code == 200
    assert len(available.json()) == 2
