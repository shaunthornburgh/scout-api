from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import outcodes, sources, seen

app = FastAPI(title="Scout API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(outcodes.router)
app.include_router(sources.router)
app.include_router(seen.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "scout-api"}
