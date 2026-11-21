"""Initial schema: outcodes, sources, seen_listings

Revision ID: 001_initial
Revises: 
Create Date: 2026-11-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outcodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("outcode", sa.String(length=10), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=True),
        sa.Column("min_psf", sa.Integer(), nullable=True),
        sa.Column("priority", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("outcode"),
    )
    op.create_index("ix_outcodes_outcode", "outcodes", ["outcode"])

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("url_or_search", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("region_filter", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sources_name", "sources", ["name"])
    op.create_index("ix_sources_type", "sources", ["type"])
    op.create_index("ix_sources_category", "sources", ["category"])
    op.create_index("ix_sources_priority", "sources", ["priority"])

    op.create_table(
        "seen_listings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("listing_id", sa.String(length=200), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("postcode", sa.String(length=20), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("source_name", sa.String(length=200), nullable=True),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="seen"),
        sa.Column("last_price", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("scout_name", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index("ix_seen_listings_listing_id", "seen_listings", ["listing_id"])
    op.create_index("ix_seen_listings_url", "seen_listings", ["url"])
    op.create_index("ix_seen_listings_postcode", "seen_listings", ["postcode"])
    op.create_index("ix_seen_listings_status", "seen_listings", ["status"])
    op.create_index("ix_seen_url_status", "seen_listings", ["url", "status"])


def downgrade() -> None:
    op.drop_index("ix_seen_url_status", table_name="seen_listings")
    op.drop_index("ix_seen_listings_status", table_name="seen_listings")
    op.drop_index("ix_seen_listings_postcode", table_name="seen_listings")
    op.drop_index("ix_seen_listings_url", table_name="seen_listings")
    op.drop_index("ix_seen_listings_listing_id", table_name="seen_listings")
    op.drop_table("seen_listings")
    op.drop_index("ix_sources_priority", table_name="sources")
    op.drop_index("ix_sources_category", table_name="sources")
    op.drop_index("ix_sources_type", table_name="sources")
    op.drop_index("ix_sources_name", table_name="sources")
    op.drop_table("sources")
    op.drop_index("ix_outcodes_outcode", table_name="outcodes")
    op.drop_table("outcodes")
