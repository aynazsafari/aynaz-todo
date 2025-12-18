from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.db.mongo import get_db
from app.models.task import TaskCreate, TaskStatusUpdate, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

router = APIRouter()


def get_service() -> TaskService:
    repo = TaskRepository(get_db())
    return TaskService(repo)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, svc: TaskService = Depends(get_service)):
    doc = await svc.create(payload)
    return {"data": doc}


@router.get("/tasks")
async def list_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status_: str | None = Query(default=None, alias="status"),
    q: str | None = Query(default=None, description="Search in title"),
    svc: TaskService = Depends(get_service),
):
    return await svc.list(limit=limit, offset=offset, status=status_, q=q)


@router.get("/tasks/{task_id}")
async def get_task(task_id: str, svc: TaskService = Depends(get_service)):
    doc = await svc.get(task_id)
    return {"data": doc}


@router.patch("/tasks/{task_id}")
async def patch_task(task_id: str, payload: TaskUpdate, svc: TaskService = Depends(get_service)):
    doc = await svc.update(task_id, payload)
    return {"data": doc}


@router.patch("/tasks/{task_id}/status")
async def patch_task_status(task_id: str, payload: TaskStatusUpdate, svc: TaskService = Depends(get_service)):
    doc = await svc.set_status(task_id, payload.status)
    return {"data": doc}


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, svc: TaskService = Depends(get_service)):
    await svc.soft_delete(task_id)
    return None
