import json
from datetime import datetime

import src.api.users.views


def test_single_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return {
            "id": 1,
            "username": "test_user",
            "email": "test_user@test.com",
            "created_date": datetime.now(),
        }

    monkeypatch.setattr(src.api.users.views, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "test_user" in data["username"]
    assert "test_user@test.com" in data["email"]
    assert "password" not in data


def test_single_user_incorrect_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(src.api.users.views, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, monkeypatch):
    def mock_get_all_users():
        return [
            {
                "id": 1,
                "username": "test_user_1",
                "email": "test_user_1@test.com",
                "created_date": datetime.now(),
            },
            {
                "id": 1,
                "username": "test_user_2",
                "email": "test_user_2@test.com",
                "created_date": datetime.now(),
            },
        ]

    monkeypatch.setattr(src.api.users.views, "get_all_users", mock_get_all_users)
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "test_user_1" in data[0]["username"]
    assert "test_user_1@test.com" in data[0]["email"]
    assert "test_user_2" in data[1]["username"]
    assert "test_user_2@test.com" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]
