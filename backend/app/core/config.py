from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = ""
    ALADIN_API_KEY: str = ""
    HUGGINGFACEHUB_API_TOKEN: str = ""
    
    # Supabase Settings
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = "" # Use Service Role Key for backend operations
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"), 
        env_file_encoding="utf-8"
    )

settings = Settings()
