
import pytest


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# --------------------------------------------------
# CREATE TASK
# --------------------------------------------------

def test_create_task(client):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn Docker",
            "description": "Understand Docker fundamentals"
        }
    )

    assert response.status_code == 201

    data = response.json()

    # PostgreSQL generates IDs using an identity sequence.
    assert isinstance(data["id"], int)
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Understand Docker fundamentals"


@pytest.mark.parametrize(
    "payload",
    [
        {"description": "Missing title"},
        {"title": "Missing description"},
        {},
        {"title": "Task without description", "description": None},
        {"title": None, "description": "Task without title"}
    ],
    ids=[
        "missing-title",
        "missing-description",
        "empty-payload",
        "null-description",
        "null-title"
    ]
)
def test_create_task_invalid_payload(client, payload):
    response = client.post(
        "/api/v1/tasks",
        json=payload
    )

    assert response.status_code == 422


# --------------------------------------------------
# GET TASKS
# --------------------------------------------------

def test_get_all_tasks(client):
    client.post(
        "/api/v1/tasks",
        json={
            "title": "Task A",
            "description": "First task"
        }
    )

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Task A"


def test_get_task_by_id(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task B",
            "description": "Second task"
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Task B"


def test_get_nonexistent_task(client):
    response = client.get("/api/v1/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# --------------------------------------------------
# UPDATE TASK — PUT
# --------------------------------------------------

def test_put_replace_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Old title",
            "description": "Old description"
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New description"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["description"] == "New description"


def test_put_nonexistent_task(client):
    response = client.put(
        "/api/v1/tasks/999",
        json={
            "title": "Updated task",
            "description": "This task does not exist"
        }
    )

    assert response.status_code == 404


# --------------------------------------------------
# UPDATE TASK — PATCH
# --------------------------------------------------

def test_patch_partial_update(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Original title",
            "description": "Original description"
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={
            "description": "Updated description"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Original title"
    assert response.json()["description"] == "Updated description"


def test_patch_nonexistent_task(client):
    response = client.patch(
        "/api/v1/tasks/999",
        json={
            "description": "Updated description"
        }
    )

    assert response.status_code == 404


# --------------------------------------------------
# DELETE TASK
# --------------------------------------------------

def test_delete_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to delete",
            "description": "Temporary task"
        }
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 404

