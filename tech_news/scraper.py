import requests
import time

from tech_news.database import create_news

from parsel import Selector


# Requisito 1
# https://www.tecmundo.com.br/novidades
# fetch("https://www.tecmundo.com.br/novidades")


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if not response.status_code == 200:
            return None
        return response.text
    except requests.Timeout:
        return None


# Requisito 2


def scrape_novidades(html_content):

    selector = Selector(text=html_content)

    href = selector.css(
        ".tec--list--lg h3.tec--card__title > a ::attr(href)"
    ).getall()
    return href


# Requisito 3
def scrape_next_page_link(html_content):

    selector = Selector(text=html_content)

    href = selector.css(".tec--list.tec--list--lg > a ::attr(href)").get()
    return href


# Requisito 4


def url_selector(html_content):
    selector = Selector(text=html_content)
    return selector.css("head > link[rel=canonical] ::attr(href)").get()


def title_selector(html_content):
    selector = Selector(text=html_content)
    return selector.css("#js-article-title ::text").get()


def timestamp_selector(html_content):
    selector = Selector(text=html_content)
    return selector.css("#js-article-date ::attr(datetime)").get()


def write_selector(html_content):
    selector = Selector(text=html_content)
    query_selectors = [
        ".tec--timestamp__item.z--font-bold ::text",
        ".tec--author__info__link ::text",
        "div > p.z--m-none.z--truncate.z--font-bold::text",
    ]

    for query in query_selectors:
        write = selector.css(query).get()
        if write is not None:
            return write.strip()
    return None


def shares_count_selector(html_content):
    selector = Selector(text=html_content)
    shares_count = selector.css(".tec--toolbar > div:nth-child(1)::text").get()
    if shares_count is not None:
        result = shares_count.strip().split(" ")[0]
        return int(result)
    return 0


# Agradecimentos a Denis Rossati >>
# https://github.com/tryber/sd-010-b-tech-news/pull/37/commits/ec2dc88e860b2fe62d1d298d5cdc9a738c10123f
def summary_selector(html_content):
    selector = Selector(text=html_content)
    return "".join(
        selector.css(".tec--article__body > p:nth-child(1) *::text").getall()
    )


def sources_selector(html_content):
    selector = Selector(text=html_content)
    query_selectors = [
        ".z--mb-16 > div > a ::text",
        ".z--mb-16.z--px-16 > div ::text",
    ]
    for query in query_selectors:
        sources = selector.css(query).getall()
        if sources is not []:
            remove_spaces_sources = list(map(lambda x: x.strip(), sources))
            return list(filter(lambda x: x != "", remove_spaces_sources))
    return None


def categories_selector(html_content):
    selector = Selector(text=html_content)
    select_categories = selector.css("#js-categories ::text").getall()
    remove_spaces_categories = list(
        map(lambda x: x.strip(), select_categories)
    )
    return list(filter(lambda x: x != "", remove_spaces_categories))


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    data = {}

    data["url"] = url_selector(html_content)
    data["title"] = title_selector(html_content)
    data["timestamp"] = timestamp_selector(html_content)
    data["writer"] = write_selector(html_content)
    data["shares_count"] = shares_count_selector(html_content)

    data["comments_count"] = int(
        selector.css("#js-comments-btn ::attr(data-count)").get()
    )
    data["summary"] = summary_selector(html_content)

    data["sources"] = sources_selector(html_content)

    data["categories"] = categories_selector(html_content)

    return data


# REF: https://www.kite.com/python/answers/
# how-to-remove-empty-strings-from-a-list-of-strings-in-python


# Requisito 5
def get_tech_news(amount):
    # html_content > novidades > pegar qtd = amount >
    # se o valor amount for maior > acionar scrape_next_page_link
    # > pegar valor restante e adicionar ao array >
    # scrape_noticia > adicionar no mongodb
    # .extends / .append
    url = "https://www.tecmundo.com.br/novidades"
    html_content = fetch(url)
    new_urls = scrape_novidades(html_content)

    tech_news = []

    while len(new_urls) < amount:
        next_page = scrape_next_page_link(html_content)
        html_content = fetch(next_page)
        new_urls.extend(scrape_novidades(html_content))

    for index in range(amount):
        new_url = new_urls[index]
        new_page = fetch(new_url)
        new_info = scrape_noticia(new_page)
        tech_news.append(new_info)

    create_news(tech_news)

    return tech_news
