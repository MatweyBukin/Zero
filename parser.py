import aiohttp
from bs4 import BeautifulSoup

HABR_URL = 'https://habr.com/ru/news/rated0/'
ARTICLE_URL = 'https://habr.com/ru/companies/selectel/news/{0}/'

async def parse_all() -> list[dict]:
    """Парсит новости из хабра
    Returns:
        Список постов в формате
        [{"title": title, "content" : content, "image" : image, "id" : article_id, "votes" : votes}, ...]"""
    
    result = []
    async with aiohttp.ClientSession() as session: #Инициализируем сессию aiohttp
        async with session.get(HABR_URL) as resp: #Запрос страницы с новостями
            html = await resp.text() #Получение html-кода
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article") #Находим все статьи на странице

            for article in articles:
                votes = int(article.find("span", class_="tm-votes-meter__value").get_text()) #Голоса за пост
                article_id = article.get("id") #Id поста
                title : str = article.find("a", class_="tm-title__link").get_text() #Заголовок
                async with session.get(ARTICLE_URL.format(article_id)) as resp: #Запрашиваем полный текст поста
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    content : str = soup.find("div", class_="article-formatted-body").get_text() #Полный текст
                try:
                    image : str = article.find("img", class_="lead-image").get("src") #Картинка
                except AttributeError:
                    image = None #Если фото нет, то None
                
                result.append({"title": title, "content" : content, "image" : image, "id" : article_id, "votes" : votes})
    return result
