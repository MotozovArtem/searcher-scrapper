#!/usr/bin/python3

import os
import sys
import argparse
import logging as log
from urllib.parse import urlparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapper.Searcher import Searcher, USER_AGENT
from scrapper.spider.spiders.quotes_spider import Spider


def main(keywords: tuple = ("займ"), count: int = 5, demo: bool = False):
    '''
    keywords: tuple (по умолчанию "займ") - кортеж ключевых слов для запроса к информационно поисковой системе\n
    count: int (по умолчанию 5) - число, ограничивающее количество сайтов, которое необходимо обработать\n
    demo: bool (по умолчанию False) - флаг, предписывающий использовать демо режим

    демо режим - запрос к инф. поисковой системе не отправляется, начинается процесс сборки данных на демо сайтах.\n
    "http://quotes.toscrape.com", "http://books.toscrape.com/
    "'''
    result = []
    if demo:
        result = ["http://quotes.toscrape.com", "http://books.toscrape.com/"]
        # result = ["https://car.bistrodengi.ru/"
        #   "https://creditplus.ru/",
        #   "https://web-zaim.ru/",
        #   "https://turbozaim.ru/",
        #   "https://dozarplati.com/",
        #   "https://fastmoney.ru/",
        #   "https://www.kredito24.ru/",
        # ]
    else:    
        search = Searcher()
        user_agent = USER_AGENT[0]
        log.debug(f"Set User-Agent header as {user_agent}")
        search.set_headers({"User-Agent": user_agent})

        log.info(f"Started searching with query {' '.join(keywords)}")
        result = search.search(keywords)

    if len(result) == 0:
        log.warning("Result is empty. Check logs")
        sys.exit(0)

    log.info(f"Searcher result:\n{os.linesep.join(result)}",'\n------------------' * 3,"\n")

    log.info(f"Limiting search result with {count} sites")
    result = result[:count]

    log.info(f"Searcher result after limitin:\n{os.linesep.join(result)}",'\n------------------' * 3,"\n")

    Spider.start_urls = result
    Spider.allowed_domains = [urlparse(url).hostname for url in result]
    Spider.max_sites = count
    process = CrawlerProcess(get_project_settings())
    process.crawl(Spider)
    process.start()


if __name__ == '__main__':
    main()
