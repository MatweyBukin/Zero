import aiohttp
from bs4 import BeautifulSoup
import json

def add_id(id):
    with open("used.json", "r") as fp:
        data = json.load(fp)
    data.append(id)
    with open("used.json", "w") as fp:
        data = json.dump(data, fp)

def check_id(id):
    with open("used.json", "r") as fp:
        data = json.load(fp)
    return id in data

HABR_URL = 'https://habr.com/ru/news/'

async def parse_one(min_votes=3):
    async with aiohttp.ClientSession() as session:
        async with session.get(HABR_URL) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article")
            for article in articles:
                votes = int(article.find("span", class_="tm-votes-meter__value").get_text())
                article_id = article.get("id")
                if votes>=min_votes and not check_id(article_id):
                    add_id(article_id)
                    title : str = article.find("a", class_="tm-title__link").get_text()
                    content : str = article.find("div", class_="article-formatted-body").get_text()
                    image : str | None = article.find("img", class_="lead-image").get("src")
                    return title, content, image
            return None