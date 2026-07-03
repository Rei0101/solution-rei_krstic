from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str | None = None


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    page: int
    size: int
