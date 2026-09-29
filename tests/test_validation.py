import pytest
from pydantic import ValidationError

from app.schemas import AssetCreate, AssignmentRequest


def test_asset_tag_requires_real_value():
    with pytest.raises(ValidationError):
        AssetCreate(
            asset_tag="",
            serial_number="SN-1",
            manufacturer="Dell",
            model="Latitude",
            location="HQ",
        )


def test_assignment_requires_person_and_location():
    with pytest.raises(ValidationError):
        AssignmentRequest(assigned_to="", location="HQ")
