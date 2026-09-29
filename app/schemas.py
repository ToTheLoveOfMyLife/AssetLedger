from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AssetStatus = Literal["AVAILABLE", "ASSIGNED", "REPAIR", "RETIRED"]


class AssetCreate(BaseModel):
    asset_tag: str = Field(min_length=2, max_length=40)
    serial_number: str = Field(min_length=2, max_length=120)
    manufacturer: str = Field(min_length=2, max_length=80)
    model: str = Field(min_length=1, max_length=120)
    location: str = Field(default="Unassigned", min_length=2, max_length=120)


class AssetPatch(BaseModel):
    manufacturer: str | None = Field(default=None, min_length=2, max_length=80)
    model: str | None = Field(default=None, min_length=1, max_length=120)
    location: str | None = Field(default=None, min_length=2, max_length=120)
    status: AssetStatus | None = None


class AssignmentRequest(BaseModel):
    assigned_to: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=120)


class RepairRequest(BaseModel):
    details: str = Field(min_length=5, max_length=1000)


class AssetEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_type: str
    details: str
    created_at: datetime


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_tag: str
    serial_number: str
    manufacturer: str
    model: str
    status: str
    assigned_to: str | None
    location: str
    created_at: datetime
    updated_at: datetime
