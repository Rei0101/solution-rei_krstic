from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.database import Base, SessionLocal, engine
from src.routers import tickets
from src.services.sync import sync_tickets


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    async with SessionLocal() as db:
        await sync_tickets(db)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "TicketHub API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(tickets.router)
