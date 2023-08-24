from libsql_client import Client, create_client
from rip_bot.config import DB_AUTH_TOKEN, DB_URL


class DatabaseClient:
    @classmethod
    def get_client(cls) -> Client:
        return create_client(url=DB_URL, auth_token=DB_AUTH_TOKEN)
