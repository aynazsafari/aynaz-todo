from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.domain.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_at: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[int] = None
    due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    limit: int
    offset: int
    total: int


class ListMeta(BaseModel):
    pagination: PaginationMeta
