from aiogram import types, Router
from aiogram.filters import Command
from db import create_user, get_user
from config import BOT_ID, DEFAULT_LANGUAGE
from bot.translation import texts

start_router: Router = Router()

@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    language = message.from_user.language_code if message.from_user.language_code is not None else DEFAULT_LANGUAGE

    user = await get_user(telegram_id, BOT_ID)
    if user is None:
        user = await create_user(telegram_id, BOT_ID, first_name, language, last_name, username)
        await message.answer(texts.WELCOME.value)
    else:
        await message.answer(texts.WELCOME_BACK.value)