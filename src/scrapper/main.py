#!/usr/bin/python3
import argparse
import logging
import sys
from urllib.parse import urlparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapper.Searcher import Searcher, USER_AGENT
from scrapper.spider.spiders.quotes_spider import Spider

# args_parser = argparse.ArgumentParser(description="Illegal activity main script")
# args_parser.add_argument("-ll", "--log_level", type=str, default="INFO", help="Log level (default: INFO)")
# args_parser.add_argument("-q", "--query", type=str, default="займ", help="Query to search (default: займ)")
# args_parser.add_argument("-s", "--size", type=int, default=10, help="Max search result size (default: 10)")

# args = args_parser.parse_args()

def main():
    # logging.basicConfig(filename="app.log",
    #                     format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
    #                     level=logging._nameToLevel[args.log_level])

    # logging.info("Started")
    search = Searcher()
    user_agent = USER_AGENT[0]
    logging.debug("Set User-Agent header as %s", user_agent)
    search.set_headers({"User-Agent": user_agent})

    query = ["займ"]
    logging.info("Started searching with query %s", " ".join(query))
    result = search.search(query)

    # if len(result) == 0:
    #     logging.warning("Result is empty. Check logs")
    #     sys.exit(0)

    # result = ["http://quotes.toscrape.com", "http://books.toscrape.com/"]
    result = ["https://car.bistrodengi.ru/"
            #   "https://creditplus.ru/",
            #   "https://web-zaim.ru/",
            #   "https://turbozaim.ru/",
            #   "https://dozarplati.com/",
            #   "https://fastmoney.ru/",
            #   "https://www.kredito24.ru/",
              ]

    Spider.start_urls = result
    Spider.allowed_domains = [urlparse(url).hostname for url in result]
    process = CrawlerProcess(get_project_settings())
    process.crawl(Spider)
    process.start()


if __name__ == '__main__':
    main()
