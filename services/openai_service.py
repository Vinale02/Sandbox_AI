from openai import AsyncOpenAI
from config import TOKEN_GPT_AI
import logging

client = AsyncOpenAI(api_key=TOKEN_GPT_AI)
MODEL = 'gpt-4o-mini'


logger = logging.getLogger(__name__)


async def ask_gpt(
        user_message: str,
        system_prompt: str = 'Ты полезный ассистент. Отвечай кратко и по делу',
        history: list = None
)-> str:

    try:
        messages = [{'role': 'system', 'content': system_prompt}]

        if history:
            valid_history = [
                item for item in history
                if isinstance(item, dict) and 'role' in item and 'content' in item
            ]
            messages.extend(valid_history)
        messages.append({'role': 'user', 'content': user_message})
        logger.info(f'GPT запрос {user_message[:20]}')

        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.8
        )
        answer = response.choices[0].message.content
        logger.info(f'Ответ GPT {len(answer)} символов')
        return answer
    except Exception as e:
        logger.error(f'Ошибка GPT {e}')
        return 'Ошибка при обращении к GPT. Попробуй ещё раз'
