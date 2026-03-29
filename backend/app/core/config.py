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
    ADMIN_SECRET_KEY: str = "" # Required in production
    ENV: str = "production"     # "development" to skip some strict checks
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"), 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

def validate_required_settings() -> None:
    """Fail-fast validation: ensure essential secrets are configured."""
    missing = []
    if not settings.SUPABASE_URL: missing.append("SUPABASE_URL")
    if not settings.SUPABASE_SERVICE_KEY: missing.append("SUPABASE_SERVICE_KEY")
    
    # Requirement: ADMIN_SECRET_KEY must be set unless explicitly in development mode
    if not settings.ADMIN_SECRET_KEY and settings.ENV != "development":
        missing.append("ADMIN_SECRET_KEY")
        
    if missing:
        raise RuntimeError(
            f"Required settings missing: {', '.join(missing)}. "
            "Please configure them in your environment or .env file."
        )
