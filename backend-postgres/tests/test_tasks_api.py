def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_task(client):
    payload = {"title": "Buy milk", "priority": 2}
    r = client.post("/api/v1/tasks", json=payload)
    assert r.status_code == 201
    data = r.json()["data"]
    assert data["title"] == "Buy milk"
    assert data["status"] == "TODO"
    task_id = data["id"]

    r2 = client.get(f"/api/v1/tasks/{task_id}")
    assert r2.status_code == 200
    assert r2.json()["data"]["id"] == task_id


def test_validation_error(client):
    r = client.post("/api/v1/tasks", json={"title": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["type"] == "validation-error"
    assert any(e["field"] == "title" for e in body.get("errors", []))


def test_list_filter_pagination(client):
    # create a few tasks
    for i in range(5):
        client.post("/api/v1/tasks", json={"title": f"Task {i}", "priority": 1})

    r = client.get("/api/v1/tasks?limit=2&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert "data" in body
    assert "meta" in body
    assert body["meta"]["pagination"]["limit"] == 2
    assert len(body["data"]) <= 2


def test_update_status_and_delete(client):
    r = client.post("/api/v1/tasks", json={"title": "Finish project"})
    task_id = r.json()["data"]["id"]

    # update
    r2 = client.patch(f"/api/v1/tasks/{task_id}", json={"description": "SRS + UML", "priority": 5})
    assert r2.status_code == 200
    assert r2.json()["data"]["priority"] == 5

    # change status
    r3 = client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "DONE"})
    assert r3.status_code == 200
    assert r3.json()["data"]["status"] == "DONE"

    # delete
    r4 = client.delete(f"/api/v1/tasks/{task_id}")
    assert r4.status_code == 204

    # should not be found (soft-deleted)
    r5 = client.get(f"/api/v1/tasks/{task_id}")
    assert r5.status_code == 404
