import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_ID", "").split(",") if x.strip()]
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


settings = Settings()
