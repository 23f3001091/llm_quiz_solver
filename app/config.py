import os
from dataclasses import dataclass

@dataclass
class Settings:
    SECRET_KEY: str
    OPENAI_API_KEY: str

def load_settings():
    return Settings(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret"),
        OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY", "")
    )
