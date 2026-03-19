from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.talk import cmd_talk
from keyboards.inline import main_menu
from handlers.random_fact import send_random_fact
from handlers.gpt_chat import cmd_gpt
from handlers.quiz import cmd_quiz
from handlers.translate import cmd_translate


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    keyboard = main_menu()
    await message.answer(f'Привет, <b>{message.from_user.first_name or "Пользователь"}</b>\n\n'
                         'Я бот с ChatGPT. Выбери, что тебя интересует.', reply_markup=keyboard, parse_mode='html')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '<b>Команды:</b>\n\n'
        '/start - Главное меню\n'
        '/random - Случайный факт\n'
        '/gpt - Диалог с ChatGPT\n'
        '/talk - Диалог с известной личностью\n'
        '/quiz - Квиз'
        '/help - Это сообщение',
        parse_mode='html'
    )


@router.callback_query(F.data == 'menu:random')
async def om_menu_random(callback: CallbackQuery):
    await callback.answer()
    await send_random_fact(callback.message)


@router.callback_query(F.data == 'menu:gpt')
async def om_menu_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_gpt(callback.message, state)


@router.callback_query(F.data == 'menu:talk')
async def om_menu_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_talk(callback.message, state)



@router.callback_query(F.data == 'menu:quiz')
async def om_menu_random(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_quiz(callback.message, state)


@router.callback_query(F.data == 'menu:translate')
async def om_menu_translate(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_translate(callback.message, state)
