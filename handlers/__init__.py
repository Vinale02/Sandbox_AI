from aiogram import Router
from handlers.command_handlers import router as command_router

router = Router()

router.include_router(command_router)