import joblib
from pathlib import Path
import pandas as pd
import numpy as np
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

    def _get_expected_columns(self):
        if hasattr(self.model, "named_steps") and "preprocessor" in self.model.named_steps:
            preprocessor = self.model.named_steps["preprocessor"]
            if hasattr(preprocessor, "feature_names_in_"):
                return list(preprocessor.feature_names_in_)
        return []

    @staticmethod
    def _resolve_aliases(input_data: dict, required_columns: list[str]) -> dict:
        row = dict(input_data)
        if "sex" in required_columns and "sex" not in row:
            row["sex"] = row.get("gender")
        if "gender" in required_columns and "gender" not in row:
            row["gender"] = row.get("sex")

        if "smoker" in required_columns and "smoker" not in row:
            row["smoker"] = row.get("discount_eligibility")
        if "discount_eligibility" in required_columns and "discount_eligibility" not in row:
            row["discount_eligibility"] = row.get("smoker")
        return row

    def predict(self, input_data: dict):
        try:
            expected_columns = self._get_expected_columns()
            row = self._resolve_aliases(input_data, expected_columns)

            if expected_columns:
                for col in expected_columns:
                    if col not in row:
                        row[col] = np.nan
                df = pd.DataFrame([[row[col] for col in expected_columns]], columns=expected_columns)
            else:
                df = pd.DataFrame([row])

            prediction = self.model.predict(df)
            return float(prediction[0])
        except Exception as e:
            logger.error("Prediction failed", exc_info=True)
            raise e

    def model_info(self) -> dict:
        return {
            "model_path": str(self.model_path),
            "exists": self.model_path.exists(),
            "expected_columns": self._get_expected_columns(),
        }
