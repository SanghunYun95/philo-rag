from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = ""
    ALADIN_API_KEY: str = ""
    
    # Supabase Settings
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = "" # Use Service Role Key for backend operations
    
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()
