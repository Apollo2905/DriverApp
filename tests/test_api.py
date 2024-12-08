# import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_power_on_route():
    response = client.post("/channel/1/on", json={"voltage": 5.0, "current": 1.0})
    assert response.status_code == 200
    assert response.json()["message"] == "Канал включен"


def test_power_off_route():
    response = client.post("/channel/1/off")
    assert response.status_code == 200
    assert response.json()["message"] == "Канал выключен"


def test_channel_state_route():
    response = client.get("/channel/1/state")
    assert response.status_code == 200
    assert "Канал" in response.json()
    assert "Состояние" in response.json()
