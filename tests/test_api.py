from fastapi.testclient import TestClient
from pathlib import Path

from src.api.main import app
from src.models.train import ModelTrainer
from src.config import Config

# Ensure model exists before testing API
def setup_module(module):
    model_path = Path(Config().get("paths")["model_save_path"])
    if not model_path.exists():
        trainer = ModelTrainer()
        trainer.train()

client = TestClient(app)

def test_homepage_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_prediction_endpoint():
    response = client.post(
        "/predict",
        json={
            "age": 30,
            "gender": "male",
            "bmi": 28.5,
            "children": 1,
            "discount_eligibility": "no",
            "region": "southwest"
        }
    )

    assert response.status_code == 200
    assert "predicted_expenses" in response.json()


def test_prediction_endpoint_with_legacy_schema():
    response = client.post(
        "/predict",
        json={
            "age": 30,
            "sex": "male",
            "bmi": 28.5,
            "children": 1,
            "smoker": "no",
            "region": "southwest"
        }
    )

    assert response.status_code == 200
    assert "predicted_expenses" in response.json()


def test_model_info_endpoint():
    response = client.get("/model-info")

    assert response.status_code == 200
    payload = response.json()
    assert payload["exists"] is True
    assert isinstance(payload["expected_columns"], list)

