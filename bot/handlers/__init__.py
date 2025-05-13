from aiogram import Router
from .start import start_router

routers: Router = Router(name="main")
routers.include_routers(start_router)