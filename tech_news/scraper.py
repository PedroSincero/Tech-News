import requests
import time

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
# #js-main > div > div > div.z--col.z--w-2-3 > div.tec--list.tec--list--lg ::a
# .tec--list--lg > a ::attr(href)


def scrape_novidades(html_content):
    # response = fetch(html_content)

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
def scrape_noticia(html_content):

    selector = Selector(text=html_content)
    data = {}

    data["url"] = selector.css("head > link[rel=canonical] ::attr(href)").get()
    data["title"] = selector.css("#js-article-title ::text").get()
    data["timestamp"] = selector.css("#js-article-date ::attr(datetime)").get()
    data["writer"] = (
        selector.css(".tec--author__info__link ::text").get().strip()
    )
    write = selector.css(".tec--author__info__link ::text").get().strip()
    data["shares_count"] = int(
        selector.css(".tec--toolbar > div:nth-child(1) ::text")
        .get()
        .split()[0]
    )
    data["comments_count"] = int(selector.css(
        "#js-comments-btn ::attr(data-count)"
    ).get())
    data["summary"] = "".join(
        selector.css(
            ".tec--article__body.z--px-16.p402_premium > p:nth-child(1) ::text"
        ).getall()
    )
    select_sources = selector.css(".z--mb-16.z--px-16 > div ::text").getall()
    remove_spaces_sources = list(
        map(lambda x: x.strip(), select_sources)
    )
    data["sources"] = list(filter(lambda x: x != "", remove_spaces_sources))
    select_categories = selector.css("#js-categories ::text").getall()
    remove_spaces_categories = list(
        map(lambda x: x.strip(), select_categories)
    )
    data["categories"] = list(
        filter(lambda x: x != "", remove_spaces_categories)
    )

    return data


# REF: https://www.kite.com/python/answers/
# how-to-remove-empty-strings-from-a-list-of-strings-in-python


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
