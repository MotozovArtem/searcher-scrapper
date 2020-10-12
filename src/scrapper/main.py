#!/usr/bin/python3
import argparse
import logging as log
import sys
from urllib.parse import urlparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapper.Searcher import Searcher, USER_AGENT
from scrapper.spider.spiders.quotes_spider import Spider


def main(keywords: tuple = ("займ"), count: int = 5, demo: bool = False):
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
        log.debug("Set User-Agent header as %s", user_agent)
        search.set_headers({"User-Agent": user_agent})

        log.info("Started searching with query %s", " ".join(keywords))
        result = search.search(keywords)

    if len(result) == 0:
        log.warning("Result is empty. Check logs")
        sys.exit(0)

    log.info("Searcher result: \n%s\n------------------\n------------------\n------------------\n", "\n".join(result))

    log.info("Limiting search result with %d sites", count)
    result = result[:count]

    log.info("Searcher result after limitin: \n%s\n------------------\n------------------\n------------------\n", "\n".join(result))


    Spider.start_urls = result
    Spider.allowed_domains = [urlparse(url).hostname for url in result]
    Spider.max_sites = count
    process = CrawlerProcess(get_project_settings())
    process.crawl(Spider)
    process.start()


if __name__ == '__main__':
    main()
