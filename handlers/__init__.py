from aiogram import Router
from handlers.command_handlers import router as command_router
from handlers.random_fact import router as random_fact_router
from handlers.gpt_chat import router as gpt_router
from handlers.talk import router as talk_router

router = Router()

router.include_routers(command_router, random_fact_router, gpt_router, talk_router)