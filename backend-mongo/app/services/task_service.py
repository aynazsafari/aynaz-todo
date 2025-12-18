from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.models.task import TaskCreate, TaskUpdate, TaskStatus
from app.repositories.task_repository import TaskRepository


class NotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create(self, payload: TaskCreate):
        now = datetime.now(timezone.utc)
        doc = {
            "id": str(uuid4()),
            "title": payload.title,
            "description": payload.description,
            "priority": payload.priority,
            "status": TaskStatus.TODO.value,
            "due_date": payload.due_date,
            "created_at": now,
            "updated_at": now,
            "deleted_at": None,
        }
        await self.repo.insert(doc)
        return doc

    async def get(self, task_id: str):
        doc = await self.repo.get_by_id(task_id)
        if not doc:
            raise NotFoundError(f"Task '{task_id}' not found.")
        return doc

    async def list(self, *, limit: int, offset: int, status: str | None, q: str | None):
        return await self.repo.list(limit=limit, offset=offset, status=status, q=q)

    async def update(self, task_id: str, payload: TaskUpdate):
        existing = await self.repo.get_by_id(task_id)
        if not existing:
            raise NotFoundError(f"Task '{task_id}' not found.")

        patch = payload.model_dump(exclude_unset=True)
        patch["updated_at"] = datetime.now(timezone.utc)

        updated = await self.repo.update(task_id, patch)
        if not updated:
            raise NotFoundError(f"Task '{task_id}' not found.")
        return updated

    async def set_status(self, task_id: str, status: TaskStatus):
        updated = await self.repo.update(task_id, {"status": status.value, "updated_at": datetime.now(timezone.utc)})
        if not updated:
            raise NotFoundError(f"Task '{task_id}' not found.")
        return updated

    async def soft_delete(self, task_id: str):
        updated = await self.repo.update(
            task_id,
            {"deleted_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)},
        )
        if not updated:
            raise NotFoundError(f"Task '{task_id}' not found.")
        return None
