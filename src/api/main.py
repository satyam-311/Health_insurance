from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.schema import InsuranceRequest
from src.models.predict import ModelPredictor

app = FastAPI()
frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir / "static"), name="static")

predictor = None


def get_predictor():
    global predictor
    if predictor is None:
        predictor = ModelPredictor()
    return predictor


@app.post("/predict")
def predict(request: InsuranceRequest):
    try:
        model = get_predictor()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    input_data = request.to_model_input()
    try:
        prediction = model.predict(input_data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {"predicted_expenses": prediction}


@app.get("/model-info")
def model_info():
    try:
        model = get_predictor()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return model.model_info()


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(frontend_dir / "index.html")

