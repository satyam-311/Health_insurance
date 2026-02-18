from fastapi import FastAPI
from src.api.schema import InsuranceRequest
from src.models.predict import ModelPredictor

app = FastAPI()

predictor = None


def get_predictor():
    global predictor
    if predictor is None:
        predictor = ModelPredictor()
    return predictor


@app.post("/predict")
def predict(request: InsuranceRequest):
    model = get_predictor()
    input_data = request.model_dump()
    prediction = model.predict(input_data)

    return {"predicted_expenses": prediction}

