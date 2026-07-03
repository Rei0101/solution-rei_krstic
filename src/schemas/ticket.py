from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str | None = None
