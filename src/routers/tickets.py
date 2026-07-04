from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
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

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/search", response_model=TicketListResponse)
async def search_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ticket).where(Ticket.title.ilike(f"%{q}%"))
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
        raise HTTPException(status_code=404, detail="Ticket not found")

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

    query = select(Ticket)

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
    ticket = Ticket(
        title=ticket_data.title,
        status=ticket_data.status,
        priority=ticket_data.priority,
        description=ticket_data.description,
        assignee=ticket_data.assignee,
        raw_source={},
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
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    updates = ticket_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(ticket, field, value)

    await db.commit()
    await db.refresh(ticket)

    return ticket
