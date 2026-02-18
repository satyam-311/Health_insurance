import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.logger import logger
from src.config import Config


class FeatureEngineering:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.config = Config()

    def build_pipeline(self):
        numeric_features = ["age", "bmi", "children"]
        categorical_features = ["gender", "discount_eligibility", "region"]

        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median"))
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ]
        )

        return preprocessor

    def split_data(self):
        test_size = self.config.get("model")["test_size"]
        random_state = self.config.get("model")["random_state"]

        X = self.df.drop(columns=["expenses"])
        y = self.df["expenses"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state
        )

        logger.info("Train-test split completed.")
        return X_train, X_test, y_train, y_test
