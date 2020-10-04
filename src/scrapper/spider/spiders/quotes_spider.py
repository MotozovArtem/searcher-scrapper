import json
import logging
import uuid
from urllib.parse import urlparse, urljoin

import scrapy
from bs4 import BeautifulSoup
from scrapy import signals

from model.DomainClasses import OrganizationProcessing


class CollectedDataByOrganizationJSON:
    collection_id: str
    url: str
    resources: list

    def __init__(self):
        self.collection_id = str(uuid.uuid4())
        self.url = str()
        self.resources = list()


class Spider(scrapy.Spider):
    name = 'illegal-activities'
    start_urls = []
    organization_processing_by_domain = dict()
    collected_data_by_domain = dict()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Spider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signal=signals.engine_stopped)
        return spider

    def spider_close(self):
        logging.info("Spider closed")
        logging.info("Saving collected data")
        for domain in self.organization_processing_by_domain.keys():
            logging.info("Saving for " + domain)
            self.organization_processing_by_domain[domain].phase = "CREATED"
            self.organization_processing_by_domain[domain].collected_data.new_file(encoding="utf-8")
            collected_data = self.collected_data_by_domain[domain]
            self.organization_processing_by_domain[domain].collected_data.write(json.dumps(collected_data.__dict__,
                                                                                           ensure_ascii=False))
            self.organization_processing_by_domain[domain].collected_data.close()
            self.organization_processing_by_domain[domain].save()

    def parse(self, response):
        parsed_url = urlparse(response.url)

        if parsed_url.hostname not in self.collected_data_by_domain:
            self.collected_data_by_domain[parsed_url.hostname] = CollectedDataByOrganizationJSON()
            self.collected_data_by_domain[parsed_url.hostname].url = \
                "{url.scheme}://{url.hostname}".format(url=parsed_url)

        if parsed_url.hostname not in self.organization_processing_by_domain.keys():
            self.organization_processing_by_domain[parsed_url.hostname] = OrganizationProcessing()

        resource = {"resource": parsed_url.path, "data": response.text}
        self.collected_data_by_domain[parsed_url.hostname].resources.append(resource)

        # Парсим HTML страницу, для того, чтобы вытащить все имеющиеся на странице ссылки
        soup = BeautifulSoup(response.text, "lxml")

        # находим все ссылки на странице
        urls = soup.find_all('a', href=True)
        for url in urls:
            yield scrapy.Request(urljoin(response.url, url["href"]), self.parse)
