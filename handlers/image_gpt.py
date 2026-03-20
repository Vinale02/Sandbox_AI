import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
import os
from states.state import ImageStates
from aiogram.enums import ChatAction
from services.openai_service import photo_processing
from keyboards.inline import main_menu, image_gpt_keyboard


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('image'))
async def cmd_image_gpt(message: Message, state: FSMContext):
    await state.set_state(ImageStates.sending)
    try:
        photo = FSInputFile('images/image_gpt.png')
        await message.answer_photo(photo=photo,
                                   caption=(
                                       '<b>Анализ изображений</b>\n\n'
                                       'Отправь любое изображение - получи текстовое описание\n'
                                   ), reply_markup=image_gpt_keyboard())
    except Exception as e:
        await message.answer(text=('<b>Анализ изображений</b>\n\n'
                                   'Отправь любое изображение - получи текстовое описание\n'
                                ), reply_markup=image_gpt_keyboard())


@router.message(ImageStates.sending, F.photo)
async def analys_image(message: Message, bot: Bot):
    photo = message.photo[-1]
    file_id = photo.file_id

    file = await bot.get_file(file_id)
    destination = f'data/temp_images/{file_id}.jpg'
    await bot.download_file(file.file_path, destination)

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    image_description = await photo_processing(destination)
    await message.answer(image_description, reply_markup=image_gpt_keyboard())
    os.remove(destination)


@router.callback_query(F.data == 'image_gpt:stop')
async def on_image_gpt_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима "Анализ изображений"')

    await callback.message.answer(text='Режим "Анализ изображений" завершен.\n\n<b>Главное меню:</b>', reply_markup=main_menu())