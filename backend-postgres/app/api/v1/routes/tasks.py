from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.enums import TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate, TaskStatusUpdate
from app.services.task_service import TaskService, ListQuery

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _service(db: Session) -> TaskService:
    return TaskService(TaskRepository(db))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    service = _service(db)
    task = service.create_task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_at=payload.due_at,
    )
    return {"data": TaskOut.model_validate(task)}


@router.get("", status_code=status.HTTP_200_OK)
def list_tasks(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_: Optional[TaskStatus] = Query(default=None, alias="status"),
    q: Optional[str] = Query(default=None, max_length=200),
    sort_by: str = Query("created_at", max_length=30),
    sort_dir: str = Query("desc", max_length=4, pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    service = _service(db)
    items, total = service.list_tasks(
        ListQuery(limit=limit, offset=offset, status=status_, q=q, sort_by=sort_by, sort_dir=sort_dir)
    )
    return {
        "data": [TaskOut.model_validate(t) for t in items],
        "meta": {"pagination": {"limit": limit, "offset": offset, "total": total}},
    }


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: str, db: Session = Depends(get_db)):
    service = _service(db)
    task = service.get_task(task_id)
    return {"data": TaskOut.model_validate(task)}


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    service = _service(db)
    patch = payload.model_dump(exclude_unset=True)
    task = service.update_task(task_id, patch)
    return {"data": TaskOut.model_validate(task)}


@router.patch("/{task_id}/status", status_code=status.HTTP_200_OK)
def change_status(task_id: str, payload: TaskStatusUpdate, db: Session = Depends(get_db)):
    service = _service(db)
    task = service.change_status(task_id, payload.status)
    return {"data": TaskOut.model_validate(task)}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    service = _service(db)
    service.delete_task(task_id)
    return None
