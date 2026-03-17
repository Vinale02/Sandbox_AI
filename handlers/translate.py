import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile, CallbackQuery
from states.state import TranslateStates
from keyboards.inline import main_menu, choose_language_keyboard
from utils.quiz_generate import send_next_question, check_answer


router = Router()
logger = logging.getLogger(__name__)


LANGUAGES = {
    'rus': {
        'name': 'русский',
        'prompt': (
            'Ты занимаешься переводом текстов. '
            'Переведи сообщение на русский язык. '
            'Ответ должен содержать только оригинальное сообщение переведенное на русский язык.'
        )
    },
    'eng': {
        'name': 'английский',
        'prompt': (
            'Ты занимаешься переводом текстов. '
            'Переведи сообщение на английский язык. '
            'Ответ должен содержать только оригинальное сообщение переведенное на английский язык.'
        )
    }
}


@router.message(Command('translate'))
async def cmd_translate(message: Message, state: FSMContext):
    await state.set_state(TranslateStates.choosing_language)

    try:
        photo = FSInputFile('images/translate.png')
        await message.answer_photo(photo=photo, caption='<b>Переводчик</b>\n\nВыберите язык перевода:', reply_markup=choose_language_keyboard())
    except Exception as e:
        await message.answer('<b>Переводчик</b>\n\nВыберите язык перевода:', reply_markup=choose_language_keyboard())


@router.callback_query(TranslateStates.choosing_language, F.data.startswith('translate:lang'))
async def on_lang_choosen(callback: CallbackQuery, state: FSMContext):
    lang_key = callback.data.split(':')[-1]

    if lang_key not in LANGUAGES:
        await callback.answer('Неизвестный язык')

    lang = LANGUAGES[lang_key]

    await state.update_data(lang=lang)
    await state.set_state(TranslateStates.answering)

    await callback.answer('')
