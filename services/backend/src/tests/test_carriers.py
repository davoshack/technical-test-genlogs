import json
from datetime import datetime

import src.api.carriers.views


def test_single_carrier(test_app, monkeypatch):
    def mock_get_carrier_by_id(carrier_id):
        return {
            "id": 1,
            "name": "test_carrier",
            "created_date": datetime.now(),
        }

    monkeypatch.setattr(
        src.api.carriers.views, "get_carrier_by_id", mock_get_carrier_by_id
    )
    client = test_app.test_client()
    resp = client.get("/carriers/1")
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert "test_carrier" in data["name"]


def test_single_carrier_incorrect_id(test_app, monkeypatch):
    def mock_get_carrier_by_id(carrier_id):
        return None

    monkeypatch.setattr(
        src.api.carriers.views, "get_carrier_by_id", mock_get_carrier_by_id
    )
    client = test_app.test_client()
    resp = client.get("/carriers/999")
    data = json.loads(resp.data)
    assert resp.status_code == 404
    assert "Carrier 999 does not exist" in data["message"]


def test_all_carriers(test_app, monkeypatch):
    def mock_get_all_carriers():
        return [
            {
                "id": 1,
                "name": "test_carrier_1",
                "created_date": datetime.now(),
            },
            {
                "id": 1,
                "name": "test_carrier_2",
                "created_date": datetime.now(),
            },
        ]

    monkeypatch.setattr(
        src.api.carriers.views, "get_all_carriers", mock_get_all_carriers
    )
    client = test_app.test_client()
    resp = client.get("/carriers")
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert len(data) == 2
    assert "test_carrier_1" in data[0]["name"]
    assert "test_carrier_2" in data[1]["name"]
