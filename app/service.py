from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Asset, AssetEvent
from .schemas import AssetCreate, AssetPatch, AssignmentRequest, RepairRequest


class AssetNotFoundError(Exception):
    pass


class InvalidAssetTransitionError(Exception):
    pass


class DuplicateAssetError(Exception):
    pass


def _record(db: Session, asset: Asset, event_type: str, details: str) -> None:
    db.add(AssetEvent(asset=asset, event_type=event_type, details=details))


def create_asset(db: Session, payload: AssetCreate) -> Asset:
    asset = Asset(**payload.model_dump())
    db.add(asset)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateAssetError("Asset tag and serial number must be unique.") from exc

    _record(db, asset, "CREATED", f"Asset {asset.asset_tag} was added to inventory.")
    db.commit()
    db.refresh(asset)
    return asset


def list_assets(db: Session, status: str | None = None, search: str | None = None) -> list[Asset]:
    statement = select(Asset).order_by(Asset.created_at.desc())

    if status:
        statement = statement.where(Asset.status == status)

    if search:
        needle = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Asset.asset_tag.ilike(needle),
                Asset.serial_number.ilike(needle),
                Asset.manufacturer.ilike(needle),
                Asset.model.ilike(needle),
                Asset.assigned_to.ilike(needle),
            )
        )

    return list(db.scalars(statement).all())


def get_asset(db: Session, asset_id: int) -> Asset:
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise AssetNotFoundError(f"Asset {asset_id} was not found.")
    return asset


def patch_asset(db: Session, asset_id: int, payload: AssetPatch) -> Asset:
    asset = get_asset(db, asset_id)
    changes = payload.model_dump(exclude_none=True)

    if asset.status == "RETIRED" and changes.get("status") not in (None, "RETIRED"):
        raise InvalidAssetTransitionError("Retired assets cannot return to active inventory.")

    for key, value in changes.items():
        setattr(asset, key, value)

    if changes:
        _record(db, asset, "UPDATED", "Updated fields: " + ", ".join(sorted(changes.keys())))

    db.commit()
    db.refresh(asset)
    return asset


def assign_asset(db: Session, asset_id: int, payload: AssignmentRequest) -> Asset:
    asset = get_asset(db, asset_id)
    if asset.status == "RETIRED":
        raise InvalidAssetTransitionError("Retired assets cannot be assigned.")

    asset.status = "ASSIGNED"
    asset.assigned_to = payload.assigned_to
    asset.location = payload.location
    _record(db, asset, "ASSIGNED", f"Assigned to {payload.assigned_to} at {payload.location}.")
    db.commit()
    db.refresh(asset)
    return asset


def mark_repair(db: Session, asset_id: int, payload: RepairRequest) -> Asset:
    asset = get_asset(db, asset_id)
    if asset.status == "RETIRED":
        raise InvalidAssetTransitionError("Retired assets cannot be moved into repair.")

    asset.status = "REPAIR"
    _record(db, asset, "REPAIR", payload.details)
    db.commit()
    db.refresh(asset)
    return asset


def retire_asset(db: Session, asset_id: int) -> Asset:
    asset = get_asset(db, asset_id)
    if asset.status == "RETIRED":
        return asset

    asset.status = "RETIRED"
    asset.assigned_to = None
    _record(db, asset, "RETIRED", "Asset retired from active inventory.")
    db.commit()
    db.refresh(asset)
    return asset


def get_events(db: Session, asset_id: int) -> list[AssetEvent]:
    asset = get_asset(db, asset_id)
    return list(asset.events)
