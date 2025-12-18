from app.services.task_service import TaskService, ListQuery, NotFoundError
from app.repositories.task_repository import TaskRepository
from app.domain.enums import TaskStatus
from app.db.session import SessionLocal, Base, engine


def setup_module(module):
    # ensure tables exist (startup not run here)
    Base.metadata.create_all(bind=engine)


def test_service_crud():
    db = SessionLocal()
    try:
        service = TaskService(TaskRepository(db))

        t = service.create_task(title="Service Task", description=None, priority=None, due_at=None)
        assert t.status == TaskStatus.TODO

        got = service.get_task(t.id)
        assert got.id == t.id

        items, total = service.list_tasks(ListQuery(limit=10, offset=0))
        assert total >= 1

        updated = service.update_task(t.id, title="Updated", description="Desc", priority=3, due_at=None)
        assert updated.title == "Updated"

        updated2 = service.change_status(t.id, TaskStatus.DONE)
        assert updated2.status == TaskStatus.DONE

        service.delete_task(t.id)
        try:
            service.get_task(t.id)
            assert False, "Expected NotFoundError"
        except NotFoundError:
            assert True
    finally:
        db.close()
