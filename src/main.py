import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from src.db.database import SessionLocal
from src.models.ticket import Ticket
from src.routers import tickets
from src.services.sync import sync_tickets
from src.utils.exceptions import (
    ServiceUnavailableError,
    register_error_handlers,
)
from src.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with SessionLocal() as db:
        logger.info("Checking database state for initial sync...")
        exists = await db.execute(select(Ticket.id).limit(1))
        first = exists.scalar_one_or_none()

        if first is None:
            try:
                logger.info("Database is empty. Initiating sync...")
                await sync_tickets(db)
                logger.info("Sync completed successfully.")
            except ServiceUnavailableError as e:
                logger.error(
                    f"Initial sync failed due to external provider: {e}"
                )
            except Exception as e:
                logger.error(
                    f"Initial sync failed due to unexpected error: {e}",
                    exc_info=True,
                )

    yield


app = FastAPI(lifespan=lifespan)

register_error_handlers(app)


@app.get("/")
async def root():
    return {"message": "TicketHub API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(tickets.router)
