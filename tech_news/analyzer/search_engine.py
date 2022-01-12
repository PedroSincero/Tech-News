import re
from tech_news.database import db
from datetime import datetime

# Requisito 6


def search_by_title(title):

    # >> ref https://github.com/tryber/sd-010-b-tech-news/pull/37/
    # commits/543324da3b2df4bbcc831b62619e04deef202b46
    find_title = list(
        db.news.find({"title": re.compile(title, re.IGNORECASE)})
    )
    result = []
    for search_title in find_title:
        result.append((search_title["title"], search_title["url"]))
    return result


# Requisito 7
def search_by_date(date):
    try:
        # ref https://www.programiz.com/python-programming/datetime/strptime
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    # ref >> https://docs.mongodb.com/manual/reference/operator/query/regex/
    find_date = list(db.news.find({"timestamp": {"$regex": date}}))

    result = []
    for search in find_date:
        result.append((search["title"], search["url"]))
    return result


# Requisito 8
def search_by_source(source):
    # sources
    find_source = list(
        db.news.find({"sources": re.compile(source, re.IGNORECASE)})
    )
    print(find_source)

    result = []
    for search in find_source:
        result.append((search["title"], search["url"]))
    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
