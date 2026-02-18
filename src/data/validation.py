from src.logger import logger
import pandas as pd


class DataValidation:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate_columns(self):
        required_columns = [
            "age",
            "gender",
            "bmi",
            "children",
            "discount_eligibility",
            "region",
            "expenses",
            "premium",
        ]

        missing_cols = set(required_columns) - set(self.df.columns)

        if missing_cols:
            logger.error(f"Missing columns: {missing_cols}")
            raise ValueError(f"Missing columns: {missing_cols}")

        logger.info("All required columns are present.")

    def validate_nulls(self):
        if self.df.isnull().sum().any():
            logger.error("Dataset contains null values.")
            raise ValueError("Dataset contains null values.")
        logger.info("No null values found.")

    def run_validation(self):
        self.validate_columns()
        self.validate_nulls()
        logger.info("Data validation completed successfully.")
