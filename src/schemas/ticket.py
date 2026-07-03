from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str | None = None
    model_config = {"from_attributes": True}


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    page: int
    size: int


class TicketDetailResponse(BaseModel):
    raw_source: dict
