import joblib
from pathlib import Path
import pandas as pd
from src.config import Config
from src.logger import logger


class ModelPredictor:
    def __init__(self):
        self.config = Config()
        self.model_path = Path(self.config.get("paths")["model_save_path"])
        self.model = self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError("Trained model not found. Train model first.")
        logger.info(f"Loading model from {self.model_path}")
        return joblib.load(self.model_path)

    def predict(self, input_data: dict):
        try:
            df = pd.DataFrame([input_data])
            prediction = self.model.predict(df)
            return float(prediction[0])
        except Exception as e:
            logger.error("Prediction failed", exc_info=True)
            raise e
