import logging as log
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

import exceptions

# User-Agent header for HTTP request
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19"
)


class Type:
    '''
    Класс-перечисление. \n
    Доступные значения:\n 
    YANDEX = 1\n 
    GOOGLE = 2\n 
    DUCK_DUCK_GO = 3
    '''
    YANDEX: int = 1
    GOOGLE: int = 2
    DUCK_DUCK_GO: int = 3


class Searcher:
    '''Класс инкапсулирующий обращение к информационно-поисковой системе'''

    def __init__(self, header: dict = None, searcher_type: Type = Type.YANDEX):
        '''
        header: dict - HTTP заголовки. User-Agent заголовок обязателен\n
        searcher_type: Type - какую инф. поиск. систему необходимо использовать. 
        По умолчанию Type.YANDEX.
        '''
        if searcher_type != Type.YANDEX:
            raise exceptions.NotSupportedSearcherTypeException(
                "Not supported searcher. Use YANDEX search engine")

        log.info("Initializing searcher")
        self.url = "https://yandex.ru/search/?text={0}"
        self.query = None
        if header is not None:
            if "User-Agent" not in header.keys():
                raise KeyError
        self.request_headers = None
        self.search_type = searcher_type

    def get_query(self) -> list:
        '''Возвращает ключевые слова'''
        return self.query

    def search(self, query: list) -> list:
        '''Отправка запроса к поисковой системе с задаными ключевые словами\n
        query: list - список ключевых слов\n
        
        Возвращает список сайтов, которые выдала инф. поисковая система'''
        log.info("Start searching")
        self.query = [str(elem) for elem in query]
        request_url = self.url.format("+".join(self.query))
        log.info("Searching URL %s", request_url)
        response = requests.get(request_url, headers=self.request_headers)

        result = []

        log.info("Response code %s", response.status_code)
        # HTTP OK = 200
        if response.status_code == HTTPStatus.OK:
            soup = BeautifulSoup(response.content, "html.parser")
            for title in soup.find_all("h2", class_="organic__title-wrapper"):
                anchors = title.find_all("a")
                if anchors:
                    link = anchors[0]["href"]
                    result.append(link)

        log.info("Clearing search result from AD references")
        result = self.__clear_ads_references(result)
        return result

    def set_headers(self, headers):
        '''Установка HTTP заголовка запроса.\n
         User-Agent обязательный заголовок'''
        if "User-Agent" not in headers.keys():
            raise KeyError()
        self.request_headers = headers

    def __clear_ads_references(self, search_result: list) -> list:
        '''Очищает результат запроса к инф. поисковой системе, от рекламных ссылок.\n
        В данный момент поддерживает только YANDEX 
        
        search_result: list - результат запрос к инф. поисковой системе
        Возвращает список сайтов (list), без рекламных ссылок'''
        if self.search_type == Type.YANDEX:
            # In Yandex responses that AD contains yabs domain
            return list(filter(lambda site: "yabs." not in site, search_result))
        else:
            return search_result
