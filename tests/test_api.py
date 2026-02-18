from fastapi.testclient import TestClient
from src.api.main import app
from src.models.train import ModelTrainer

# Ensure model exists before testing API
def setup_module(module):
    trainer = ModelTrainer()
    trainer.train()

client = TestClient(app)

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

