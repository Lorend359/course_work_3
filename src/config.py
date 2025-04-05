import os
from dotenv import load_dotenv

load_dotenv()

HH_API_URL = os.getenv("HH_API_URL", "https://api.hh.ru")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
