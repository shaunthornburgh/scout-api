from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OutcodeBase(BaseModel):
    outcode: str
    region: Optional[str] = None
    min_psf: Optional[int] = None
    priority: bool = True
    notes: Optional[str] = None
    active: bool = True


class OutcodeCreate(OutcodeBase):
    pass


class OutcodeUpdate(BaseModel):
    region: Optional[str] = None
    min_psf: Optional[int] = None
    priority: Optional[bool] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class OutcodeOut(OutcodeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class SourceBase(BaseModel):
    name: str
    type: str  # portal | auction | receiver
    category: Optional[str] = None
    priority: int = 3
    url_or_search: Optional[str] = None
    active: bool = True
    notes: Optional[str] = None
    region_filter: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[int] = None
    url_or_search: Optional[str] = None
    active: Optional[bool] = None
    notes: Optional[str] = None
    region_filter: Optional[str] = None


class SourceOut(SourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class SeenBase(BaseModel):
    listing_id: Optional[str] = None
    url: str
    address: Optional[str] = None
    postcode: Optional[str] = None
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    status: str = "seen"
    last_price: Optional[str] = None
    notes: Optional[str] = None
    scout_name: Optional[str] = None


class SeenCreate(SeenBase):
    pass


class SeenUpdate(BaseModel):
    status: Optional[str] = None
    last_price: Optional[str] = None
    notes: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    last_seen: Optional[datetime] = None


class SeenOut(SeenBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_seen: datetime
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
