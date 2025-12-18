from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional, Tuple

from sqlalchemy import select, func, asc, desc
from sqlalchemy.orm import Session

from app.domain.models import Task
from app.domain.enums import TaskStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id, Task.deleted_at.is_(None))
        return self.db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        *,
        limit: int,
        offset: int,
        status: Optional[TaskStatus] = None,
        q: Optional[str] = None,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ) -> Tuple[list[Task], int]:
        stmt = select(Task).where(Task.deleted_at.is_(None))

        if status is not None:
            stmt = stmt.where(Task.status == status)

        if q:
            # simple title search (case-insensitive on supported DBs)
            stmt = stmt.where(Task.title.ilike(f"%{q}%"))

        # total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = int(self.db.execute(count_stmt).scalar_one())

        # sorting
        allowed = {
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
            "due_at": Task.due_at,
            "priority": Task.priority,
            "title": Task.title,
            "status": Task.status,
        }
        sort_col = allowed.get(sort_by, Task.created_at)
        order_fn = desc if sort_dir.lower() == "desc" else asc

        stmt = stmt.order_by(order_fn(sort_col)).limit(limit).offset(offset)
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def update(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def soft_delete(self, task: Task) -> None:
        task.deleted_at = utc_now()
        self.db.add(task)
        self.db.commit()
