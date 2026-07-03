from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import Base, engine
from src.models.ticket import Ticket
from src.routers import tickets


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    yield
    # shutdown (optional cleanup)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "TicketHub API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(tickets.router)