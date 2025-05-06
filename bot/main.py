import logging, sys

from fastapi import FastAPI, APIRouter

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.exceptions import TelegramRetryAfter
from aiogram_fastapi_server import SimpleRequestHandler, setup_application

from db import init_db
from bot.handlers import start_router
from config import BOT_TOKEN, REDIS_URL
from config import ( WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_PATH, 
    ALLOWED_UPDATES, MAX_CONNECTIONS, DROP_PENDING_UPDATES
)

api_router  = APIRouter()
@api_router .get("/ping")
async def pong():
    return {"response": "pong"}

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main_startup(bot: Bot):
    try:
        await bot.set_webhook(
            url=WEBHOOK_URL.rstrip("/") + WEBHOOK_PATH,
            allowed_updates=ALLOWED_UPDATES,
            max_connections=MAX_CONNECTIONS,
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=DROP_PENDING_UPDATES 
        )
    except TelegramRetryAfter as e:
        logging.warning(f"Bot webhook not set, retry after: {e.retry_after}")
    except Exception as e:
        logging.error(e)

def register_main_bot(dp: Dispatcher, app: FastAPI, bot: Bot, **kwargs):
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)
dp.startup.register(main_startup)
app = FastAPI()
app.include_router(api_router)
bot = Bot(token=BOT_TOKEN)
dp.include_routers(start_router)

logging.getLogger('aiogram').setLevel(logging.WARNING)

@app.on_event("startup")
async def on_startup():
    logging.info("Init started")
    await init_db()
    logging.info("Init finished")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Shutdown started")
    try:
        await bot.delete_webhook()
    except TelegramRetryAfter as e:
        logging.warning(f"Bot webhook not deleted, retry after: {e.retry_after}")
    except Exception as e:
        logging.error(e)
    logging.info("Shutdown finished")

register_main_bot(dp, app, bot)