import mlflow
import mlflow.sklearn
import joblib
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from pathlib import Path

from src.logger import logger
from src.config import Config
from src.data.ingestion import DataIngestion
from src.data.validation import DataValidation
from src.features.build_features import FeatureEngineering


class ModelTrainer:
    def __init__(self):
        self.config = Config()
        self.model_params = self.config.get("model")
        self.model_save_path = Path(self.config.get("paths")["model_save_path"])

    def train(self):
        ingestion = DataIngestion()
        df = ingestion.load_data()

        validator = DataValidation(df)
        validator.run_validation()

        feature_engineering = FeatureEngineering(df)
        X_train, X_test, y_train, y_test = feature_engineering.split_data()

        preprocessor = feature_engineering.build_pipeline()

        model = XGBRegressor(
            n_estimators=self.model_params["n_estimators"],
            learning_rate=self.model_params["learning_rate"],
            max_depth=self.model_params["max_depth"],
            random_state=self.model_params["random_state"]
        )

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

        mlflow.set_experiment("insurance_expense_prediction")

        with mlflow.start_run():
            pipeline.fit(X_train, y_train)

            predictions = pipeline.predict(X_test)

            mse = mean_squared_error(y_test, predictions)
            rmse = mse ** 0.5

            r2 = r2_score(y_test, predictions)

            mlflow.log_params(self.model_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2_score", r2)

            mlflow.sklearn.log_model(pipeline, "model")

            logger.info(f"RMSE: {rmse}")
            logger.info(f"R2 Score: {r2}")

            self.model_save_path.parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(pipeline, self.model_save_path)

            logger.info(f"Model saved at {self.model_save_path}")

        return rmse, r2
