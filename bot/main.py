import logging, sys

from urllib.parse import urljoin
from fastapi import FastAPI, APIRouter

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramRetryAfter
from aiogram_fastapi_server import SimpleRequestHandler, setup_application

from config import DEFAULT_LANGUAGE
i18n = I18n(path="bot/locales", default_locale=DEFAULT_LANGUAGE, domain="messages")

from db import init_db
from bot.handlers import routers
from bot.middlewares import I18nSqlMiddleware
from config import BOT_TOKEN, REDIS_URL
from config import ( WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_PATH, 
    ALLOWED_UPDATES, MAX_CONNECTIONS, DROP_PENDING_UPDATES
)

api_router  = APIRouter()
@api_router .get("/ping")
async def pong():
    return {"response": "pong"}

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(levelname)s:     %(message)s')

async def main_startup(bot: Bot):
    try:
        webhook_url = urljoin(WEBHOOK_URL.rstrip("/"), WEBHOOK_PATH)
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=ALLOWED_UPDATES,
            max_connections=MAX_CONNECTIONS,
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=DROP_PENDING_UPDATES 
        )
        logging.info(f"Webhook successfully set at {webhook_url}")
    except TelegramRetryAfter as e:
        logging.warning(f"Bot webhook not set, retry after: {e.retry_after}")
    except Exception as e:
        logging.error(e)

def register_main_bot(dp: Dispatcher, app: FastAPI, bot: Bot, **kwargs):
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)
app = FastAPI()
app.include_router(api_router)
bot = Bot(token=BOT_TOKEN)
dp.include_routers(routers)

logging.getLogger('aiogram').setLevel(logging.WARNING)

@app.on_event("startup")
async def on_startup():
    logging.info("Initialization started")
    try:
        logging.info("Database Initialization")
        await init_db()
        logging.info("Middleware Initialization")
        dp.update.middleware(I18nSqlMiddleware())
        bot_info = await bot.get_me()
        logging.info(f"Webhook bot '{bot_info.full_name}' - @{bot_info.username} [id={bot_info.id}]")
        await main_startup(bot)
        logging.info("Initialization completed successfully")
    except Exception as e:
        logging.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Shutdown started")
    try:
        bot_info = await bot.get_me()
        logging.info(f"Stopping bot '{bot_info.full_name}' - @{bot_info.username} [id={bot_info.id}]")
        await bot.delete_webhook()
    except TelegramRetryAfter as e:
        logging.warning(f"Bot webhook not deleted, retry after: {e.retry_after}")
    except Exception as e:
        logging.error(e)
    logging.info("Shutdown finished")

register_main_bot(dp, app, bot)