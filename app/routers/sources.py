from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Source
from app.schemas import SourceCreate, SourceOut, SourceUpdate

router = APIRouter(prefix="/sources", tags=["sources"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=list[SourceOut])
async def list_sources(
    active: bool | None = None,
    type: str | None = None,
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Source)
    if active is not None:
        stmt = stmt.where(Source.active == active)
    if type:
        stmt = stmt.where(Source.type == type)
    if category:
        stmt = stmt.where(Source.category == category)
    result = await db.execute(stmt.order_by(Source.priority, Source.name))
    return result.scalars().all()


@router.post("", response_model=SourceOut)
async def create_source(payload: SourceCreate, db: AsyncSession = Depends(get_db)):
    obj = Source(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{source_id}", response_model=SourceOut)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Source, source_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.patch("/{source_id}", response_model=SourceOut)
async def update_source(source_id: int, payload: SourceUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Source, source_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj
