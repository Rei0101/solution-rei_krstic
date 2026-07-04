from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from src.db.database import SessionLocal
from src.models.ticket import Ticket
from src.routers import tickets
from src.services.sync import sync_tickets


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with SessionLocal() as db:
        exists = await db.execute(select(Ticket.id).limit(1))
        first = exists.scalar_one_or_none()

        if first is None:
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
