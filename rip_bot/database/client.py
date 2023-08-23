from libsql_client import Client, create_client
from rip_bot.config import DB_AUTH_TOKEN, DB_URL


def start_client() -> Client:
    client: Client = create_client(url=DB_URL, auth_token=DB_AUTH_TOKEN)
    return client


db_client: Client = start_client()
