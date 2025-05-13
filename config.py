import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN", "12345:abcdefghijklmnopq")
BOT_ID = os.getenv("BOT_ID", "12345")

SUPPORTED_LANGUAGES = ['en', 'fa']
DEFAULT_LANGUAGE = 'en'

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your.domain.com")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "super-secret-token")

ALLOWED_UPDATES = [
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member",
    "chat_join_request",
    "message_reaction",
    "message_reaction_count",
]
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 40))
DROP_PENDING_UPDATES = os.getenv("DROP_PENDING_UPDATES", "False").lower() == "true"


WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 8081))
WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", 1))


MYSQL_USER = os.getenv("MYSQL_USER", "username")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DB = os.getenv("MYSQL_DB", "dbname")

DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)