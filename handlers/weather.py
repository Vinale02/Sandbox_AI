import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
import aiohttp
from states.state import WeatherStates
from aiogram.enums import ChatAction
from keyboards.inline import main_menu, weather_choosing_keyboard, weather_keyboard, weather_switch_city
from config import WEATHER_API


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('weather'))
async def cmd_weather(message: Message, state: FSMContext):
    await state.set_state(WeatherStates.choosing_city)

    try:
        photo = FSInputFile('images/weather.png')
        await message.answer_photo(photo=photo,
                                   caption=(
                                        '<b>Погода</b>\n\n'
                                        'Введите название своего города:'
                                   ), reply_markup=weather_keyboard())
    except Exception:
        await message.answer(text=(
                                '<b>Погода</b>\n\n'
                                'Введите название своего города:'
                                ), reply_markup=weather_keyboard())


@router.message(WeatherStates.choosing_city, F.text)
async def on_choosen_city(message: Message, state: FSMContext, session: aiohttp.ClientSession):
    await state.set_state(WeatherStates.sending)

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    city = message.text
    await state.update_data(city=city)
    await conf_city(message, state, session)


@router.message(WeatherStates.sending)
async def conf_city(message: Message, state: FSMContext, session: aiohttp.ClientSession):
    data = await state.get_data()
    city_name = data.get('city')

    try:
        photo = FSInputFile('images/weather.png')
        await message.answer_photo(photo=photo,
                                   caption=(
                                       'Подтвердите город:\n\n'
                                       f'<b>{city_name}</b>'
                                   ), reply_markup=weather_switch_city())
    except Exception:
        await message.answer(text=(
                                'Подтвердите город:\n\n'
                                f'<b>{city_name}</b>'
                            ), reply_markup=weather_switch_city())


async def get_weather(message: Message, state: FSMContext, session: aiohttp.ClientSession):
    data = await state.get_data()
    city_name = data.get('city')

    try:
        async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&lang=ru&units=metric') as response:
            return await response.json()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')


async def show_weather(message: Message, state: FSMContext, session: aiohttp.ClientSession):
    weather_data = await get_weather(message, state, session)
    data = await state.get_data()
    city = data.get('city')

    if weather_data:
        if weather_data.get('message') == 'city not found':
            try:
                await message.edit_caption(caption=('<b>ДАННОГО ГОРОДА НЕ СУЩЕСТВУЕТ</b>\n\n'
                                                    'Нажмите кнопку "Сменить город"'),
                                           reply_markup=weather_choosing_keyboard())
            except Exception:
                await message.answer(text=('<b>ДАННОГО ГОРОДА НЕ СУЩЕСТВУЕТ</b>\n\n'
                                            'Нажмите кнопку "Сменить город"'),
                                     reply_markup=weather_choosing_keyboard())
        else:
            weather_info = (
                f'☀️ <b>Текущая погода в {city}</b>:  {weather_data['weather'][0]['description']}',
                f'🌡️ <b>Температура:</b>  {weather_data['main']['temp']}°C',
                f'🔥 <b>Ощущается как:</b>  {weather_data['main']['feels_like']}°C',
                f'💧 <b>Влажность:</b>  {weather_data['main']['humidity']}%',
                f'🌪️ <b>Скорость ветра:</b>  {int(weather_data['wind']['speed'] * 3.6):.1f} км/ч'
            )

            try:
                await message.edit_caption(caption=(
                                               '\n'.join(weather_info)
                                           ), reply_markup=weather_choosing_keyboard())
            except Exception:
                await message.answer('\n'.join(weather_info), reply_markup=weather_choosing_keyboard())


@router.callback_query(F.data == 'weather:conf')
async def on_city_conf(callback: CallbackQuery, state: FSMContext, session: aiohttp.ClientSession):
    await callback.answer()
    await show_weather(callback.message, state, session)


@router.callback_query(F.data == 'weather:change_city')
async def on_change_city(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_weather(callback.message, state)


@router.callback_query(F.data == 'weather:stop')
async def on_weather_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer('Выхожу из режима "Погода"')

    await callback.message.answer(text='Режим "Погода" завершен\n\n<b>Главное меню:</b>', reply_markup=main_menu())