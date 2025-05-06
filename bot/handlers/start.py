from aiogram import types, Router
from aiogram.filters import Command
from db import create_user, get_user
from config import BOT_ID

start_router: Router = Router()

@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    user = await get_user(telegram_id, BOT_ID)
    if user is None:
        user = await create_user(telegram_id, BOT_ID, first_name, last_name, username)
        await message.answer(f"Hello, {user.first_name}! Your profile has been created.")
    else:
        await message.answer(f"Hello, {user.first_name}! welcome back.")