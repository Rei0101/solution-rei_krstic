from typing import Literal

from pydantic import BaseModel, Field


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


class TicketCreate(BaseModel):
    title: str
    status: Literal["open", "closed"]
    priority: Literal["low", "medium", "high"]
    description: str | None = Field(default="", max_length=100)
    assignee: str | None = None
