from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🎲 Случайный факт', callback_data='menu:random', style='primary')],
            [InlineKeyboardButton(text='🤖 Chat GPT', callback_data='menu:gpt', style='primary')],
            [InlineKeyboardButton(text='🗣️ Диалог с личностью', callback_data='menu:talk', style='primary')],
            [InlineKeyboardButton(text='🎯 Квиз', callback_data='menu:quiz', style='primary')],
            [InlineKeyboardButton(text='🌐 Переводчик',callback_data='menu:translate', style='primary')],
            [InlineKeyboardButton(text='🖼️ Анализ изображений', callback_data='menu:image_gpt', style='primary')]
        ]
    )


def random_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🎲 Хочу ещё факт', callback_data='random:again')],
            [InlineKeyboardButton(text='⛔ Закончить', callback_data='random:stop', style='danger')]
        ]
    )


def gpt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⛔ Закончить', callback_data='gpt:stop', style='danger')]
        ]
    )


def persons_keyboard(persons):
    buttons = [
        [InlineKeyboardButton(text=f'{data['emoji']} {data['name']}', callback_data=f'talk:person:{key}')]
        for key, data in persons.items()
    ]
    buttons.append([
        InlineKeyboardButton(text='⛔ Закончить', callback_data='talk:stop', style='danger')
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def talk_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔄 Сменить собеседника', callback_data='talk:change')],
            [InlineKeyboardButton(text='⛔ Закончить', callback_data='talk:stop', style='danger')]
        ]
    )


def quiz_topics_keyboard(topics: dict) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=data['name'], callback_data=f'quiz:topic:{key}')]
        for key, data in topics.items()
    ]
    buttons.append(
        [InlineKeyboardButton(text='⛔ Отмена', callback_data='quiz:cancel', style='danger')]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def after_answer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard= [
            [InlineKeyboardButton(text='➡️ Следующий вопрос', callback_data='quiz:next')],
            [InlineKeyboardButton(text='🔄 Сменить тему', callback_data='quiz:change_topic')],
            [InlineKeyboardButton(text='⛔ Закончить квиз', callback_data='quiz:stop', style='danger')]
        ]
    )


def choose_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard= [
            [
                InlineKeyboardButton(text='Русский', callback_data='translate:lang:rus'),
                InlineKeyboardButton(text='English', callback_data='translate:lang:eng'),
            ],
            [
                InlineKeyboardButton(text='⛔ Закончить', callback_data='translate:stop', style='danger')
            ]
        ]
    )


def translate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard= [
            [
                InlineKeyboardButton(text='🔄 Сменить язык', callback_data='translate:change_lang'),
                InlineKeyboardButton(text='⛔ Закончить', callback_data='translate:stop', style='danger')
            ]
        ]
    )


def image_gpt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard= [
            [
                InlineKeyboardButton(text='⛔ Закончить', callback_data='image_gpt:stop', style='danger')
            ]
        ]
    )