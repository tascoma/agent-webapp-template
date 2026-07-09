from pathlib import Path

from pydantic_settings import BaseSettings

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_env: str = "development"
    # Unused by the base template — reserved for session/cookie signing once
    # /add-auth wires it up. Left blank, the app still boots.
    secret_key: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
    # Plain str — pydantic-settings would JSON-decode a list[str] field before validators run.
    allowed_origins: str = "http://localhost:5173"
    # Unused until a SQLAlchemy engine is wired up (see /setup-supabase). Left
    # blank, the app still boots; the engine factory should raise a clear
    # error if this is unset once it's actually consumed.
    database_url: str = ""
    # Supabase Storage credentials — only needed if you use Supabase Storage
    # (see /setup-storage). Left blank, the base app still boots.
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    storage_bucket: str = "uploads"
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-6"
    log_level: str = "INFO"

    model_config = {"env_file": _ENV_FILE}


settings = Settings()
