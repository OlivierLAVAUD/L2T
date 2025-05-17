from pydantic_settings import BaseSettings
from pydantic import Field, validator
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # Debug
    debug: bool = Field(False, alias="DEBUG_MODE")
    log_path: Path = Field(Path("logs"), alias="LOG_PATH")
    log_file: str = Field("translation.log", alias="LOG_FILE")

    # Translation
    model_name: str = Field("facebook/nllb-200-distilled-600M", alias="MODEL_NAME")
    default_target_lang: str = Field("fra_Latn", alias="DEFAULT_TARGET_LANG")
    default_source_lang: Optional[str] = Field(None, alias="DEFAULT_SOURCE_LANG")
    max_length: int = Field(512, alias="MAX_LENGTH")
    batch_size: int = Field(8, alias="BATCH_SIZE")
    chunk_size: int = Field(400, alias="CHUNK_SIZE")

    # Performance
    use_gpu: bool = Field(True, alias="USE_GPU")
    torch_precision: str = Field("high", alias="TORCH_PRECISION")
    cache_dir: Path = Field(Path("models"), alias="CACHE_DIR")

    # Files
    encoding: str = Field("utf-8", alias="ENCODING")
    auto_output_ext: str = Field(".translated.txt", alias="OUTPUT_EXT")
    max_file_size_mb: int = Field(10, alias="MAX_FILE_SIZE_MB")

    @validator('cache_dir', 'log_path')
    def create_dirs(cls, value: Path) -> Path:
        value.mkdir(parents=True, exist_ok=True)
        return value

    @validator('max_file_size_mb')
    def convert_to_bytes(cls, v) -> int:
        return v * 1024 * 1024

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()