from fastapi import HTTPException
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.ticket import Ticket
from src.schemas.ticket import TicketListResponse, TicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=TicketListResponse)
async def get_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * size

    result = await db.execute(select(Ticket).offset(offset).limit(size))

    tickets = result.scalars().all()

    return {
        "items": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
                "description": (t.title[:100] if t.title else None),
            }
            for t in tickets
        ],
        "page": page,
        "size": size,
    }


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


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
