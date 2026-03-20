import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
import aiohttp
from aiogram.enums import ChatAction
from keyboards.inline import main_menu, cats_keyboard


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('cats'))
async def cmd_cats(message: Message, session: aiohttp.ClientSession):

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    cat_image = await get_cat(message, session)
    if cat_image:
        photo = cat_image[0]['url']
        await message.answer_photo(photo=photo, reply_markup=cats_keyboard())


async def get_cat(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            'https://api.thecatapi.com/v1/images/search') as response:
            return await response.json()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')


@router.callback_query(F.data == 'cats:again')
async def cmd_cats_again(callback: CallbackQuery, session: aiohttp.ClientSession):
    await callback.answer()
    await callback.message.delete()
    await cmd_cats(callback.message, session)


@router.callback_query(F.data == 'cats:stop')
async def cmd_cats_stop(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_caption(caption='<b>Главное меню:</b>', reply_markup=main_menu())
    except Exception:
        await callback.message.answer('<b>Главное меню:</b>', reply_markup=main_menu())