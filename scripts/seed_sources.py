"""
Seed the sources table from the three CSV files.

Usage (after migrations):
    python -m scripts.seed_sources

Expects the CSVs in ./seed_data/ relative to the project root.
"""
import asyncio
import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Source

SEED_DIR = Path(__file__).resolve().parent.parent / "seed_data"

FILES = [
    ("scout_portals_sources.csv", "portal"),
    ("scout_auction_sources.csv", "auction"),
    ("scout_receivers_sources.csv", "receiver"),
]


async def seed():
    async with AsyncSessionLocal() as db:
        for filename, source_type in FILES:
            path = SEED_DIR / filename
            if not path.exists():
                print(f"Skipping missing file: {path}")
                continue

            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = (row.get("name") or "").strip()
                    if not name:
                        continue

                    # Check if already exists by name + type
                    result = await db.execute(
                        select(Source).where(Source.name == name, Source.type == source_type)
                    )
                    existing = result.scalar_one_or_none()

                    data = {
                        "name": name,
                        "type": source_type,
                        "category": (row.get("category") or "").strip() or None,
                        "priority": int(row.get("priority") or 3),
                        "url_or_search": (row.get("url") or "").strip() or None,
                        "notes": (row.get("notes") or "").strip() or None,
                        "active": True,
                    }

                    if existing:
                        for k, v in data.items():
                            setattr(existing, k, v)
                        print(f"Updated: {source_type} / {name}")
                    else:
                        db.add(Source(**data))
                        print(f"Created: {source_type} / {name}")

        await db.commit()
        print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
