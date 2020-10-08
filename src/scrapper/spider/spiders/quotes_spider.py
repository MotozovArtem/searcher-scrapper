import json
import logging
import uuid
from urllib.parse import urlparse, urljoin

import scrapy
from bs4 import BeautifulSoup
from scrapy import signals

from model import OrganizationProcessing, Organization, CollectedDataByOrganization

import peewee


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

            collected_data = self.collected_data_by_domain[domain]
            collected_data.resources = json.dumps(
                collected_data.resources_array).encode("utf-8")
            collected_data.save()

            organization = Organization()
            organization.name = domain
            organization.save()

            self.organization_processing_by_domain[domain].organization = organization
            self.organization_processing_by_domain[domain].collected_data = collected_data
            self.organization_processing_by_domain[domain].save()

    def parse(self, response):
        parsed_url = urlparse(response.url)

        if parsed_url.hostname not in self.collected_data_by_domain:
            self.collected_data_by_domain[parsed_url.hostname] = CollectedDataByOrganization(
            )
            self.collected_data_by_domain[parsed_url.hostname].url = \
                "{url.scheme}://{url.hostname}".format(url=parsed_url)
            self.collected_data_by_domain[parsed_url.hostname].resources_array = [
            ]

        if parsed_url.hostname not in self.organization_processing_by_domain.keys():
            self.organization_processing_by_domain[parsed_url.hostname] = OrganizationProcessing(
            )

        resource = {"resource": parsed_url.path, "data": response.text}
        self.collected_data_by_domain[parsed_url.hostname].resources_array.append(
            resource)

        # Парсим HTML страницу, для того, чтобы вытащить все имеющиеся на странице ссылки
        soup = BeautifulSoup(response.text, "lxml")

        # находим все ссылки на странице
        urls = soup.find_all('a', href=True)
        for url in urls:
            yield scrapy.Request(urljoin(response.url, url["href"]), self.parse)
