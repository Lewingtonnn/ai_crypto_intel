import yaml
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel


class Config(BaseModel):
    project: Dict[str, Any]
    paths: Dict[str, Any]
    embedding: Dict[str, Any]
    database: Dict[str, Any]
    api: Dict[str, Any]
    llm: Dict[str, Any]


def load_config(config_path: str = "configs/config.yaml") -> Config:
    """Load YAML configuration and return a validated Config object."""
    try:
        # Resolve absolute path relative to project root
        project_root = Path(__file__).resolve().parents[1]
        full_path = project_root / config_path

        if not full_path.exists():
            raise FileNotFoundError(f"Config file not found at {full_path}")

        with open(full_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)

        return Config(**config_data)

    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {e}")

