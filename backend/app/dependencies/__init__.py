from supabase import Client, create_client

from app.agents.agent import agent
from app.core.config import settings


def get_agent():
    return agent


def get_storage_client() -> Client:
    if not (settings.supabase_url and settings.supabase_service_role_key):
        raise RuntimeError(
            "Supabase Storage not configured: set SUPABASE_URL and "
            "SUPABASE_SERVICE_ROLE_KEY (see /setup-storage)."
        )
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
