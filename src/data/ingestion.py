import pandas as pd
from pathlib import Path
from src.logger import logger
from src.config import Config


class DataIngestion:
    def __init__(self):
        self.config = Config()
        self.raw_data_path = Path(self.config.get("paths")["raw_data_path"])

    def load_data(self) -> pd.DataFrame:
        try:
            logger.info(f"Loading data from {self.raw_data_path}")
            df = pd.read_csv(self.raw_data_path)
            logger.info(f"Data loaded successfully with shape {df.shape}")
            return df
        except Exception as e:
            logger.error("Error occurred while loading data", exc_info=True)
            raise e
