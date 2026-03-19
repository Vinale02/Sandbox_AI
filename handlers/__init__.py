from aiogram import Router
from handlers.command_handlers import router as command_router
from handlers.random_fact import router as random_fact_router
from handlers.gpt_chat import router as gpt_router
from handlers.talk import router as talk_router
from handlers.quiz import  router as quis_router
from handlers.translate import router as translate_router
from handlers.image_gpt import router as image_gpt_router

router = Router()

router.include_routers(command_router, random_fact_router, gpt_router, talk_router, quis_router, translate_router, image_gpt_router)