from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Outcode
from app.schemas import OutcodeCreate, OutcodeOut, OutcodeUpdate

router = APIRouter(prefix="/outcodes", tags=["outcodes"], dependencies=[Depends(verify_api_key)])


@router.get("", response_model=list[OutcodeOut])
async def list_outcodes(
    active: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Outcode)
    if active is not None:
        stmt = stmt.where(Outcode.active == active)
    result = await db.execute(stmt.order_by(Outcode.outcode))
    return result.scalars().all()


@router.post("", response_model=OutcodeOut)
async def create_outcode(payload: OutcodeCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Outcode).where(Outcode.outcode == payload.outcode))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Outcode already exists")
    obj = Outcode(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{outcode_id}", response_model=OutcodeOut)
async def get_outcode(outcode_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Outcode, outcode_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.patch("/{outcode_id}", response_model=OutcodeOut)
async def update_outcode(outcode_id: int, payload: OutcodeUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Outcode, outcode_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj
