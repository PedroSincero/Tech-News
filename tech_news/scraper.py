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


def summary_selector(html_content):
    selector = Selector(text=html_content)
    summary = "".join(
        selector.css(".p402_premium > p:nth-child(1) ::text").getall()
    )
    if summary is not None:
        return summary
    return None


def summary_sources(html_content):
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

    data["sources"] = summary_sources(html_content)

    data["categories"] = categories_selector(html_content)

    return data


# REF: https://www.kite.com/python/answers/
# how-to-remove-empty-strings-from-a-list-of-strings-in-python


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
