import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

# Provider registry — add new providers here
PROVIDERS = {
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "meta/llama-3.1-70b-instruct",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "default_model": "llama3.2",
    },
}


@dataclass
class Settings:
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "LLM_BASE_URL", "http://localhost:11434/v1"
        )
    )
    api_key: str = field(
        default_factory=lambda: os.getenv("LLM_API_KEY", "")
    )
    model: str = field(
        default_factory=lambda: os.getenv(
            "LLM_MODEL", "llama3.2"
        )
    )
    max_tokens: int = 1024
    temperature: float = 0.7


def get_settings() -> Settings:
    return Settings()
