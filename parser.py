import aiohttp
from bs4 import BeautifulSoup

HABR_URL = 'https://habr.com/ru/news/rated0/'
ARTICLE_URL = 'https://habr.com/ru/companies/selectel/news/{0}/'

async def parse_all():
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(HABR_URL) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                votes = int(article.find("span", class_="tm-votes-meter__value").get_text())
                article_id = article.get("id")
                title : str = article.find("a", class_="tm-title__link").get_text()
                async with session.get(ARTICLE_URL.format(article_id)) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    content : str = soup.find("div", class_="article-formatted-body").get_text()
                try:
                    image : str = article.find("img", class_="lead-image").get("src")
                except AttributeError:
                    image = None
                
                result.append({"title": title, "content" : content, "image" : image, "id" : article_id, "votes" : votes})
    return result