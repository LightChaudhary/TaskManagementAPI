from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_existing_task():
    response = client.get("/tasks/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "title" in data

def test_get_nonexistent_task():
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "task not found!"

def test_create_task():
    task_data = {
        "title": "Learn pytest",
        "description": "Write automated tests for the API",
        "status": "todo",
        "priority": "high",
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data

def test_create_task_with_default():
    task_data = {
        "title": "Test defaults",
        "description": "Verify default status and priority",
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["status"] == "todo"
    assert data["priority"] == "medium"

def test_create_task_with_invalid_priority():
    task_data = {
        "title": "Invalid task",
        "description": "Testing validation",
        "priority": "urgent",
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 422


def test_update_existing_task():
    updated_data = {
        "title": "Updated task",
        "description": "Updated description",
        "status": "in_progress",
        "priority": "high",
    }

    response = client.put("/tasks/1", json=updated_data)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
    assert data["status"] == updated_data["status"]
    assert data["priority"] == updated_data["priority"]

def test_update_nonexistent_task():
    updated_data = {
        "title": "Updated task",
        "description": "Updated description",
        "status": "in_progress",
        "priority": "high",
    }

    response = client.put("/tasks/999", json=updated_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "task not found!"

def test_delete_existing_task():
    response = client.delete("/tasks/2")

    assert response.status_code == 204
    assert response.content == b""

def test_deleted_task_is_not_found():
    delete_response = client.delete("/tasks/2")

    assert delete_response.status_code == 204

    response = client.get("/tasks/2")

    assert response.status_code == 404

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "task not found!"

