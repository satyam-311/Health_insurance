import yaml
from pathlib import Path


class Config:
    def __init__(self, config_path: str = "config/model.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def get(self, key: str):
        return self.config.get(key)
