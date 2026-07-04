from typing import Literal

from pydantic import BaseModel, Field


class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str | None = None
    assignee: str | None = None
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


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: Literal["open", "closed"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    description: str | None = Field(default="", max_length=100)
    assignee: str | None = None
