from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any

from app.domain.models import Task
from app.domain.enums import TaskStatus
from app.repositories.task_repository import TaskRepository


class NotFoundError(Exception):
    pass


@dataclass(frozen=True)
class ListQuery:
    limit: int = 20
    offset: int = 0
    status: Optional[TaskStatus] = None
    q: Optional[str] = None
    sort_by: str = "created_at"
    sort_dir: str = "desc"


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(
        self,
        *,
        title: str,
        description: Optional[str],
        priority: Optional[int],
        due_at,
    ) -> Task:
        task = Task(
            title=title.strip(),
            description=description,
            priority=priority,
            due_at=due_at,
            status=TaskStatus.TODO,
        )
        return self.repo.create(task)

    def get_task(self, task_id: str) -> Task:
        task = self.repo.find_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task

    def list_tasks(self, query: ListQuery) -> Tuple[list[Task], int]:
        return self.repo.list(
            limit=query.limit,
            offset=query.offset,
            status=query.status,
            q=query.q,
            sort_by=query.sort_by,
            sort_dir=query.sort_dir,
        )

    def update_task(self, task_id: str, patch: Dict[str, Any]) -> Task:
        """PATCH semantics:
        - only provided fields are updated
        - provided fields may be set to None to clear optional values (e.g., description)
        """
        task = self.get_task(task_id)

        if "title" in patch and patch["title"] is not None:
            task.title = str(patch["title"]).strip()

        if "description" in patch:
            task.description = patch["description"]

        if "priority" in patch:
            task.priority = patch["priority"]

        if "due_at" in patch:
            task.due_at = patch["due_at"]

        return self.repo.update(task)

    def change_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        task.status = status
        return self.repo.update(task)

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self.repo.soft_delete(task)
