from dotenv import load_dotenv
load_dotenv() #Подгружаем файл конфига .env

from aiogram import Bot
from os import environ
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
from parser import parse_all
import ai

from id_manager import add_id, check_id

bot = Bot(environ.get("BOT_TOKEN")) #Создает бота по токену в .env

async def send_post():
    """Парсит недавнюю новость из хабра и отправляет в канал. 
Проверяет последние MAX_INDEX (.env) новостей по оценкам (больше MIN_VOTES (.env) голосов)"""

    articles = await parse_all() #Парсит из хабра новости
    article_index = 0
    while article_index<int(environ.get("MAX_INDEX")) and article_index<len(articles): #Перебираем новости
        article = articles[article_index]
        title = article["title"]
        content = article["content"]
        image = article["image"]
        article_id = article["id"]
        votes = article["votes"]

        logging.info(f"Пост:\n\n{title}\n\n{content}\n\n{votes} - {article_id}")
        print(f"Айди есть - {check_id(article_id)}")
        print(image)
        if not check_id(article_id) and votes>=int(environ.get("MIN_VOTES")) and image: #Проверка новости по критериям
            if len(content)>900: content = await ai.explain(content) #ИИ сокращает статью если текст слишком большой
            logging.info(f"Сокращенный текст:\n\n{content}")

            add_id(article_id) #Добавление новости в список отправленных

            logging.info(f"Отправляю пост - {article_id}")
            await bot.send_photo( #Отправка поста
                chat_id=environ.get("CHANNEL"),
                photo=image,
                caption=f"<b>{title}</b>\n\n{content}",
                parse_mode="HTML"
            )

            break

        article_index+=1
    else:
        logging.info("Не отправляю пост")

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
    logging.basicConfig(filename="app.log", level=logging.INFO)
    asyncio.run(main())