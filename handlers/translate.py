import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile, CallbackQuery

from services.openai_service import ask_gpt
from states.state import TranslateStates
from keyboards.inline import main_menu, choose_language_keyboard, translate_keyboard


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
        await message.answer_photo(photo=photo, caption='<b>Переводчик</b>\n\nВыберите язык перевода:',
                                   reply_markup=choose_language_keyboard())
    except Exception as e:
        await message.answer('<b>Переводчик</b>\n\nВыберите язык на который будем переводить:',
                             reply_markup=choose_language_keyboard())


@router.callback_query(TranslateStates.choosing_language, F.data.startswith('translate:lang'))
async def on_lang_choosen(callback: CallbackQuery, state: FSMContext):
    lang_key = callback.data.split(':')[-1]

    if lang_key not in LANGUAGES:
        await callback.answer('Неизвестный язык')

    lang = LANGUAGES[lang_key]

    await state.update_data(lang=lang_key)

    await callback.answer(f'Выбран {lang['name']} язык')

    await callback.message.edit_caption(
        caption=(f'Введите сообщение на любом языке и '
                f'получите его перевод на {lang['name']} язык.'
                ), reply_markup=translate_keyboard()
    )


@router.message(F.text)
async def translating(message: Message, state: FSMContext):
    data = await state.get_data()
    lang_key = data['lang']

    if lang_key not in LANGUAGES:
        await message.amswer('Что-то пошло не так. Начните заново /translate')
        await state.clear()
        return

    lang = LANGUAGES[lang_key]

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING)

    response = await ask_gpt(
        user_message=message.text,
        system_prompt=lang['prompt']
    )

    await message.answer(text=f'<b>Перевод:</b>\n\n{response}', reply_markup=translate_keyboard())


@router.callback_query(F.data == 'translate:change_lang')
async def change_lang(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TranslateStates.choosing_language)

    await callback.answer()

    try:
        photo = FSInputFile('images/translate.png')
        await callback.message.answer_photo(photo=photo, caption='<b>Переводчик</b>\n\nВыберите язык перевода:',
                                   reply_markup=choose_language_keyboard())
    except Exception as e:
        await callback.message.answer('<b>Переводчик</b>\n\nВыберите язык на который будем переводить:',
                             reply_markup=choose_language_keyboard())


@router.callback_query(F.data == 'translate:stop')
async def stop_translate(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer('Выхожу из режима "Переводчик"')

    try:
        await callback.message.edit_caption(caption='Режим "Переводчик".\n\n<b>Главное меню:</b>', reply_markup=main_menu())
    except Exception as e:
        await callback.message.edit_text(text='Режим "Переводчик" завершен.\n\n<b>Главное меню:</b>', reply_markup=main_menu())