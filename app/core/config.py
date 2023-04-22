from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseSettings


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    yaml_file = getattr(settings.__config__, "yaml_file", "")

    assert yaml_file, "Settings.yaml_file not properly configured"

    path = Path(yaml_file)

    if not path.exists():
        raise FileNotFoundError(f"Could not open yaml settings file at: {path}")
    return yaml.safe_load(path.read_text("utf-8"))


class Models(BaseSettings):
    model_path: str


class ModelConfig(BaseSettings):
    llm: Models
    embeddings: Models


class Config(BaseSettings):
    models: ModelConfig

    class Config:
        yaml_file = Path("config").resolve().joinpath("config.yaml")
        case_sensitive = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                yaml_config_settings_source,
                env_settings,
            )


config = Config()


llm_model = config.models.llm.model_path
embedding_model = config.models.embeddings.model_path
