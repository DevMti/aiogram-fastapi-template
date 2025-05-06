from aiogram import Router
from .start import start_router

routers: Router = Router(name="main")
routers.include_router(start_router)
