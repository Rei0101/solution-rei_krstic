from typing import Literal

from pydantic import BaseModel, Field


class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str = ""
    assignee: str | None = None
    model_config = {"from_attributes": True}


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    page: int
    size: int
    model_config = {"from_attributes": True}


class TicketDetailResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    description: str = ""
    assignee: str | None = None
    raw_source: dict | None = None
    model_config = {"from_attributes": True}


class TicketCreate(BaseModel):
    title: str
    status: Literal["open", "closed"]
    priority: Literal["low", "medium", "high"]
    description: str | None = Field(default=None, max_length=100)
    assignee: str | None = None


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: Literal["open", "closed"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    description: str | None = Field(default=None, max_length=100)
    assignee: str | None = None
