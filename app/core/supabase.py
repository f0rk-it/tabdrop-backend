from app.config import settings
from supabase import create_client, Client

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(url, key)