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


# result = fetch("https://www.tecmundo.com.br/novidades")

# scrape_novidades(result)
# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
