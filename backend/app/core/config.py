from pathlib import Path
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = ""
    ALADIN_API_KEY: str = ""
    HUGGINGFACEHUB_API_TOKEN: str = ""
    
    # Supabase Settings
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = Field(
        "", 
        validation_alias=AliasChoices("SUPABASE_SERVICE_KEY", "SUPABASE_SERVICE_ROLE_KEY")
    ) # Use Service Role Key for backend operations
    
    # Auth
    ADMIN_SECRET_KEY: str = "dev-secret-key" # Default for dev, override in .env
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"), 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

def validate_required_settings() -> None:
    """Fail-fast validation: ensure essential secrets are configured."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY (or SUPABASE_SERVICE_ROLE_KEY) "
            "must be configured in environment variables."
        )
