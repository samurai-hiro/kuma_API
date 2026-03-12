
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from predictor import predict

def test_predict_success(monkeypatch):
    # 外部依存をモック
    monkeypatch.setattr("predictor.get_city_code", lambda lat, lon: 123456)
    monkeypatch.setattr("predictor.fetch_estat_value", lambda **kwargs: 100 if kwargs['cat_code']=='A1101' else 10)
    monkeypatch.setattr("predictor.get_elevation", lambda lat, lon: 50)
    monkeypatch.setattr("predictor.pipemodel", type("MockPipeModel", (), {"predict": lambda self, df: [99.99]})())

    result = predict(35.0, 139.0, "2026-03-12")
    assert result["result"] == 99.99
    assert result["municd"] == 123456
    assert result["elevation"] == 50
    assert result["population_density"] is not None

def test_predict_valueerror(monkeypatch):
    monkeypatch.setattr("predictor.get_city_code", lambda lat, lon: (_ for _ in ()).throw(ValueError("not in Japan")))
    with pytest.raises(ValueError) as exc:
        predict(0, 0, "2026-03-12")
    assert "not in Japan" in str(exc.value)

def test_predict_general_exception(monkeypatch):
    monkeypatch.setattr("predictor.get_city_code", lambda lat, lon: 123456)
    monkeypatch.setattr("predictor.fetch_estat_value", lambda **kwargs: 100 if kwargs['cat_code']=='A1101' else 0)  # land_area=0でZeroDivisionError
    monkeypatch.setattr("predictor.get_elevation", lambda lat, lon: 50)
    monkeypatch.setattr("predictor.pipemodel", type("MockPipeModel", (), {"predict": lambda self, df: [99.99]})())
    with pytest.raises(Exception) as exc:
        predict(35.0, 139.0, "2026-03-12")
    assert "Error during prediction" in str(exc.value)