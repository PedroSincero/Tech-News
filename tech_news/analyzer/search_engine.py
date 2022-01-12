import re
from tech_news.database import db

# Requisito 6


def search_by_title(title):

    find_title = list(
        db.news.find({"title": re.compile(title, re.IGNORECASE)})
    )
    result = []
    for search_title in find_title:
        result.append((search_title["title"], search_title["url"]))
    return result


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
