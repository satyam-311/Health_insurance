from fastapi import FastAPI
from src.models.predict import ModelPredictor
from src.api.schema import InsuranceRequest

app = FastAPI(title="Health Insurance Expense Prediction API")

predictor = ModelPredictor()


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/predict")
def predict(request: InsuranceRequest):
    input_data = request.model_dump()
    prediction = predictor.predict(input_data)
    return {"predicted_expenses": prediction}
