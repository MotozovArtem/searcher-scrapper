import logging

import requests
from bs4 import BeautifulSoup
from http import HTTPStatus

# User-Agent header for HTTP request
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19"
)


class Searcher:
    def __init__(self, header: dict = None):
        logging.info("Initializing searcher")
        self.url = "https://yandex.ru/search/?text={0}"
        self.query = None
        if header is not None:
            if "User-Agent" not in header.keys():
                raise KeyError
        self.request_headers = None

    def get_query(self) -> list:
        return self.query

    def search(self, query: list) -> list:
        logging.info("Start searching")
        self.query = [str(elem) for elem in query]
        request_url = self.url.format("+".join(self.query))
        logging.info("Searching URL %s", request_url)
        response = requests.get(request_url, headers=self.request_headers)

        result = []

        logging.info("Response code %s", response.status_code)
        # HTTP OK = 200
        if response.status_code == HTTPStatus.OK:
            soup = BeautifulSoup(response.content, "html.parser")
            for title in soup.find_all("h2", class_="organic__title-wrapper"):
                anchors = title.find_all("a")
                if anchors:
                    link = anchors[0]["href"]
                    result.append(link)

        return result

    def set_headers(self, headers):
        if "User-Agent" not in headers.keys():
            raise KeyError
        self.request_headers = headers
