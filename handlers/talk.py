import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from states.state import TalkStates
from aiogram.enums import ChatAction
from services.openai_service import ask_gpt
from keyboards.inline import main_menu, persons_keyboard, talk_keyboard


router = Router()
logger = logging.getLogger(__name__)


PERSONS = {
    'pushkin': {
    'name': 'Александр Пушкин',
    'emoji': '🪶',
    'prompt': (
        'Ты - Александр Сергеевич Пушкин, известный русский писатель 19 века.'
        'Говори изысканно с поэтическими оборотмами.'
        'Иногда вставляй короткие стихотворные строки.'
        'Отвечай на русском языке.'
        )
    },
    'musk': {
    'name': 'Илон Маск',
    'emoji': '🚀',
    'prompt': (
        'Ты - Илон Маск, предпрениматель и визионер.'
        'Говори энергично, с энтузиазмом о технологиях и будущем.'
        'Упоминай Tesla, SpaceX, Марс, искусственный интеллект.'
        'Иногда шути. ОТвечай на русском языке.'
        )
    },
    'jobs': {
    'name': 'Стив Джобс',
    'emoji': '🍎',
    'prompt': (
        'Ты - Стив Джобс, сооснователь Apple.'
        'Говори вдохновляюще и дизайне, простоте, революции.'
        'Часто говори о перфекционизме и любви к своему делу.'
        'Отвечай на русском языке.'
        )
    }
}


@router.message(Command('talk'))
async def cmd_talk(message: Message, state: FSMContext):
    await state.set_state(TalkStates.choosing_person)

    try:
        photo = FSInputFile('images/talk.png')
        await message.answer_photo(photo=photo,
                                   caption=(
                                       '<b>Диалог с известной личностю</b>\n\n'
                                       'Выбери собеседника'
                                   ), reply_markup=persons_keyboard(PERSONS), parse_mode='html')
    except Exception as e:
        await message.answer(text='<b>Диалог с известной личностю</b>\n\n'
                                  'Выбери собеседника', reply_markup=persons_keyboard(PERSONS), parse_mode='html')


@router.callback_query(TalkStates.choosing_person, F.data.startswith('talk:person:'))
async def on_person_chosen(callback: CallbackQuery, state: FSMContext):
    person_key = callback.data.split(':')[-1]

    if person_key not in PERSONS:
        await callback.answer('Неизвестная личность')

    person = PERSONS[person_key]

    await state.update_data(person_key=person_key, history=[])
    await state.set_state(TalkStates.chatting)

    await callback.answer(f'Начинаем разговор с {person['name']}')

    await callback.message.edit_caption(
        caption=(f'{person['emoji']} <b>Вы разговариваете с {person['name']}</b>\n\n'
                 'Напишите что-нибудь и получите ответ в его стиле'
                 ), reply_markup=talk_keyboard(), parse_mode='html'
    )


@router.message(TalkStates.chatting, F.text)
async def cmd_talk_person(message: Message, state: FSMContext):
    data = await state.get_data()
    person_key = data['person_key']
    history = data.get('history', [])

    if person_key not in PERSONS:
        await message.answer('Что-то пошло не так. Начните заново /talk')
        await state.clear()
        return

    person = PERSONS[person_key]

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING)

    history.append({'role': 'user', 'content': message.text})

    response = await ask_gpt(
        user_message=message.text,
        system_prompt=person['prompt'],
        history=history[:-1]
    )

    history.append({'role': 'assistant', 'content': response})

    if len(history) > 16:
        history = history[-16:]

    await state.update_data(history=history)

    await message.answer(text=f'{person['emoji']} <b>{person['name']}</b>\n\n{response}', reply_markup=talk_keyboard(), parse_mode='html')


@router.callback_query(F.data == 'talk:stop')
async def on_talk_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима "Общение с личностью"')

    try:
        await callback.message.edit_caption(caption='Режим "Общение с личностью" завершен')
    except Exception as e:
        await callback.message.edit_text(text='Режим "Общение с личностью" завершен')