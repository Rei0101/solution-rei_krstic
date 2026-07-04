from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import func, select

from src.db.database import Base, SessionLocal, engine
from src.models.ticket import Ticket
from src.routers import tickets
from src.services.sync import sync_tickets


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        result = await db.execute(select(func.count(Ticket.id)))
        count = result.scalar()

        if count == 0:
            try:
                await sync_tickets(db)
            except Exception as e:
                print(f"Initial sync failed: {e}")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "TicketHub API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(tickets.router)
