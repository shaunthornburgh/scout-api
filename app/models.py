from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Outcode(Base):
    __tablename__ = "outcodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    outcode: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    region: Mapped[Optional[str]] = mapped_column(String(100))
    min_psf: Mapped[Optional[int]] = mapped_column(Integer)
    priority: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)  # portal | auction | receiver
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True)  # e.g. Aggregator, National auction, Commercial portal, IP property list
    priority: Mapped[int] = mapped_column(Integer, default=3, index=True)
    url_or_search: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    region_filter: Mapped[Optional[str]] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    listings: Mapped[list["SeenListing"]] = relationship(back_populates="source")


class SeenListing(Base):
    __tablename__ = "seen_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    url: Mapped[str] = mapped_column(Text, unique=True, index=True)
    address: Mapped[Optional[str]] = mapped_column(Text)
    postcode: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    source_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sources.id"))
    source_name: Mapped[Optional[str]] = mapped_column(String(200))  # denormalized for convenience
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="seen", index=True)  # seen | sent | killed | etc.
    last_price: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    scout_name: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    source: Mapped[Optional[Source]] = relationship(back_populates="listings")

    __table_args__ = (
        Index("ix_seen_url_status", "url", "status"),
    )
