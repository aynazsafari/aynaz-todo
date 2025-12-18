from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: int = Field(default=3, ge=1, le=5)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_date: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: int
    status: TaskStatus
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
