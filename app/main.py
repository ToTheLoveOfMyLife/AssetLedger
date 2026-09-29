from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .schemas import (
    AssetCreate,
    AssetEventRead,
    AssetPatch,
    AssetRead,
    AssignmentRequest,
    RepairRequest,
)
from .service import (
    AssetNotFoundError,
    DuplicateAssetError,
    InvalidAssetTransitionError,
    assign_asset,
    create_asset,
    get_asset,
    get_events,
    list_assets,
    mark_repair,
    patch_asset,
    retire_asset,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="AssetLedger API",
    version="1.0.0",
    description="IT asset lifecycle and audit-history service.",
    lifespan=lifespan,
)

Db = Annotated[Session, Depends(get_db)]


@app.exception_handler(AssetNotFoundError)
async def not_found_handler(_, exc: AssetNotFoundError):
    return _problem(status.HTTP_404_NOT_FOUND, "Asset not found", str(exc))


@app.exception_handler(InvalidAssetTransitionError)
async def transition_handler(_, exc: InvalidAssetTransitionError):
    return _problem(status.HTTP_409_CONFLICT, "Invalid lifecycle transition", str(exc))


@app.exception_handler(DuplicateAssetError)
async def duplicate_handler(_, exc: DuplicateAssetError):
    return _problem(status.HTTP_409_CONFLICT, "Duplicate asset", str(exc))


def _problem(code: int, title: str, detail: str):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=code,
        content={"type": "about:blank", "title": title, "status": code, "detail": detail},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/assets", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create(payload: AssetCreate, db: Db):
    return create_asset(db, payload)


@app.get("/api/assets", response_model=list[AssetRead])
def list_all(
    db: Db,
    status_filter: str | None = Query(default=None, alias="status"),
    search: str | None = None,
):
    return list_assets(db, status=status_filter, search=search)


@app.get("/api/assets/{asset_id}", response_model=AssetRead)
def get_one(asset_id: int, db: Db):
    return get_asset(db, asset_id)


@app.patch("/api/assets/{asset_id}", response_model=AssetRead)
def update(asset_id: int, payload: AssetPatch, db: Db):
    return patch_asset(db, asset_id, payload)


@app.post("/api/assets/{asset_id}/assign", response_model=AssetRead)
def assign(asset_id: int, payload: AssignmentRequest, db: Db):
    return assign_asset(db, asset_id, payload)


@app.post("/api/assets/{asset_id}/repair", response_model=AssetRead)
def repair(asset_id: int, payload: RepairRequest, db: Db):
    return mark_repair(db, asset_id, payload)


@app.post("/api/assets/{asset_id}/retire", response_model=AssetRead)
def retire(asset_id: int, db: Db):
    return retire_asset(db, asset_id)


@app.get("/api/assets/{asset_id}/events", response_model=list[AssetEventRead])
def events(asset_id: int, db: Db):
    return get_events(db, asset_id)
