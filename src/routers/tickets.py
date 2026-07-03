from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("")
async def create_ticket(db: AsyncSession = Depends(get_db)):
    ticket = Ticket(
        title="Test ticket",
        status="open",
        priority="medium",
        assignee=None,
    )

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    return ticket
