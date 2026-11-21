from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.models import SeenListing
from app.schemas import SeenCreate, SeenOut, SeenUpdate

router = APIRouter(prefix="/seen", tags=["seen"], dependencies=[Depends(verify_api_key)])


@router.get("/check", response_model=Optional[SeenOut])
async def check_url(url: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Return the existing record if the URL has been seen, else null."""
    result = await db.execute(select(SeenListing).where(SeenListing.url == url))
    return result.scalar_one_or_none()


@router.post("", response_model=SeenOut)
async def upsert_seen(payload: SeenCreate, db: AsyncSession = Depends(get_db)):
    """Create or update (by URL). Updates last_seen and any provided fields."""
    result = await db.execute(select(SeenListing).where(SeenListing.url == payload.url))
    existing = result.scalar_one_or_none()

    now = datetime.utcnow()
    if existing:
        data = payload.model_dump(exclude_unset=True)
        data.pop("url", None)
        for k, v in data.items():
            setattr(existing, k, v)
        existing.last_seen = now
        existing.updated_at = now
        await db.commit()
        await db.refresh(existing)
        return existing

    obj = SeenListing(**payload.model_dump(), first_seen=now, last_seen=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("", response_model=list[SeenOut])
async def list_seen(
    status: Optional[str] = None,
    postcode: Optional[str] = None,
    source_name: Optional[str] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(SeenListing)
    if status:
        stmt = stmt.where(SeenListing.status == status)
    if postcode:
        stmt = stmt.where(SeenListing.postcode.ilike(f"%{postcode}%"))
    if source_name:
        stmt = stmt.where(SeenListing.source_name.ilike(f"%{source_name}%"))
    stmt = stmt.order_by(SeenListing.last_seen.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.patch("/{seen_id}", response_model=SeenOut)
async def update_seen(seen_id: int, payload: SeenUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(SeenListing, seen_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    if "last_seen" not in payload.model_dump(exclude_unset=True):
        obj.last_seen = datetime.utcnow()
    await db.commit()
    await db.refresh(obj)
    return obj
