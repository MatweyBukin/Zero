from aiogram import Bot
from dotenv import load_dotenv
from os import environ
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
from parser import parse_one

load_dotenv() #Подгружаем файл конфига .env

bot = Bot(environ.get("BOT_TOKEN")) #Создает бота по токену в .env

async def send_post():
    """Парсит недавнюю новость из хабра и отправляет в канал"""

    title, content, image = await parse_one()
    if image:
        await bot.send_photo( #Отправка поста
            chat_id=environ.get("CHANNEL"),
            photo=image,
            caption=f"<b>{title}</b>\n\n{content}",
            parse_mode="HTML"
        )
    else:
        await bot.send_message(
            chat_id=environ.get("CHANNEL"),
            text=f"<b>{title}</b>\n\n{content}",
            parse_mode="HTML"
        )

async def main():
    scheduler = AsyncIOScheduler() #Создаем расписание

    scheduler.add_job( #Добавляем задачу
        send_post,
        trigger="interval",
        minutes=int(environ.get("INTERVAL_MIN")) #Каждые X минут из .env
    )

    scheduler.start() #Запускаем расписание

    await send_post() #Постим 1 пост сразу

    await asyncio.Event().wait()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())