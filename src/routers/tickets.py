from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.ticket import Ticket
from src.schemas.ticket import (
    TicketCreate,
    TicketDetailResponse,
    TicketListResponse,
    TicketResponse,
    TicketUpdate,
)
from src.utils.exceptions import (
    InvalidTicketOperationError,
    TicketAlreadyExistsError,
    TicketNotFoundError,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(Ticket.id)))

    open_count = await db.scalar(
        select(func.count(Ticket.id)).where(Ticket.status == "open")
    )
    closed_count = await db.scalar(
        select(func.count(Ticket.id)).where(Ticket.status == "closed")
    )

    low_count = await db.scalar(
        select(func.count(Ticket.id)).where(Ticket.priority == "low")
    )
    medium_count = await db.scalar(
        select(func.count(Ticket.id)).where(Ticket.priority == "medium")
    )
    high_count = await db.scalar(
        select(func.count(Ticket.id)).where(Ticket.priority == "high")
    )

    assignee_result = await db.execute(
        select(Ticket.assignee, func.count(Ticket.id)).group_by(
            Ticket.assignee
        )
    )

    assignees = {
        row[0] if row[0] else "unassigned": row[1]
        for row in assignee_result.all()
    }

    completion_rate = (closed_count / total) if total else 0
    open_ratio = (open_count / total) if total else 0

    return {
        "total": total,
        "status": {
            "open": open_count,
            "closed": closed_count,
        },
        "priority": {
            "low": low_count,
            "medium": medium_count,
            "high": high_count,
        },
        "ratios": {
            "open_ratio": round(open_ratio, 3),
            "completion_rate": round(completion_rate, 3),
        },
        "assignees": assignees,
    }


@router.get("/search", response_model=TicketListResponse)
async def search_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * size

    result = await db.execute(
        select(Ticket)
        .where(Ticket.title.ilike(f"%{q}%"))
        .offset(offset)
        .limit(size)
    )

    tickets = result.scalars().all()

    return TicketListResponse(
        items=[
            TicketResponse(
                id=t.id,
                title=t.title,
                status=t.status,
                priority=t.priority,
                description=t.description,
            )
            for t in tickets
        ],
        page=page,
        size=size,
    )


@router.get("/{ticket_id}", response_model=TicketDetailResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise TicketNotFoundError(ticket_id)

    return ticket


@router.get("", response_model=TicketListResponse)
async def get_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Literal["open", "closed"] | None = Query(None),
    priority: Literal["low", "medium", "high"] | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * size

    query = select(Ticket).order_by(Ticket.id.asc())

    if status:
        query = query.where(Ticket.status == status)

    if priority:
        query = query.where(Ticket.priority == priority)

    query = query.offset(offset).limit(size)

    result = await db.execute(query)
    tickets = result.scalars().all()

    return TicketListResponse(
        items=[
            TicketResponse(
                id=t.id,
                title=t.title,
                status=t.status,
                priority=t.priority,
                description=t.description,
            )
            for t in tickets
        ],
        page=page,
        size=size,
    )


@router.post("", response_model=TicketDetailResponse, status_code=201)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
):
    if hasattr(ticket_data, "id") and ticket_data.id is not None:
        existing = await db.get(Ticket, ticket_data.id)
        if existing:
            raise TicketAlreadyExistsError(ticket_data.id)

    ticket = Ticket(
        title=ticket_data.title,
        status=ticket_data.status,
        priority=ticket_data.priority,
        description=ticket_data.description,
        assignee=ticket_data.assignee,
        raw_source=ticket_data.model_dump(),
    )

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    return ticket


@router.patch("/{ticket_id}", response_model=TicketDetailResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise TicketNotFoundError(ticket_id)

    updates = ticket_data.model_dump(exclude_unset=True)

    if (
        "status" in updates
        and ticket.status == "closed"
        and updates["status"] == "closed"
    ):
        raise InvalidTicketOperationError(
            "Ticket already closed and finalized."
        )

    for field, value in updates.items():
        setattr(ticket, field, value)

    await db.commit()
    await db.refresh(ticket)

    if ticket.description is None:
        ticket.description = ""

    return ticket
