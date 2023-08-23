import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DB_URL = os.getenv("DB_URL")
DB_AUTH_TOKEN = os.getenv("DB_AUTH_TOKEN")
