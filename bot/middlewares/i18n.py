from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db import get_user
from bot.main import i18n
from config import BOT_ID, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class I18nSqlMiddleware(BaseMiddleware):
    def __init__(self, default_locale=DEFAULT_LANGUAGE):
        self.default_locale = default_locale
        self.i18n = i18n

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        data["user"] = user
        if user:
            user_data = await get_user(user.id, BOT_ID)
            if user_data is None:
                locale = user.language_code if user.language_code in SUPPORTED_LANGUAGES else self.default_locale
            else:
                locale = user_data.language if user_data.language in SUPPORTED_LANGUAGES else self.default_locale

            data["locale"] = locale 
        else:
            locale = self.default_locale
            data["locale"] = locale
            
        with self.i18n.context(), self.i18n.use_locale(locale):
            return await handler(event, data)