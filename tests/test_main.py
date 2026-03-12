import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to the kuma predictor API"}

def test_predict_valid(monkeypatch):
    # モック用関数
    def mock_predict(lat, lon, date):
        return {"result": 42}

    # predictor.predictをモック
    monkeypatch.setattr("main.predict", mock_predict)

    payload = {"lat": 35.0, "lon": 139.0, "date": "2026-03-12"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["result"] == 42

def test_predict_error(monkeypatch):
    def mock_predict(lat, lon, date):
        raise ValueError("invalid input")

    monkeypatch.setattr("main.predict", mock_predict)

    payload = {"lat": 0, "lon": 0, "date": "2026-03-12"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["result"] is None
    assert "invalid input" in response.json()["error"]
