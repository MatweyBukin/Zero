from openai import AsyncOpenAI
from os import environ

PROMPT = "Сократи текст. Ответь только текстом, без лишних фраз и без форматирования. Можешь убрать незначительные детали, чтобы текст хорошо читался ивсе было понятно.\nТекст:\n{0}"

client = AsyncOpenAI(
    api_key=environ.get("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

async def explain(article : str) -> str:
    """Сокращает текст с помощью ии
    Args:
        article: Текст для сокращения
    Returns:
        Сокращенный текст"""
    
    response = await client.responses.create(
        input=PROMPT.format(article),
        model=environ.get("AI_MODEL"),
        max_output_tokens=int(environ.get("MAX_TOKENS"))
    )
    return response.output_text