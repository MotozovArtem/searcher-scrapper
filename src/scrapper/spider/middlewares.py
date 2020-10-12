# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class QuotetutorialSpiderMiddleware(object):
    '''Описание middleware - логики промежуточных действий между запросами'''

    @classmethod
    def from_crawler(cls, crawler):
        '''Этот метод используется Scrapy для создания личных Spiders.'''
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        '''Вызывается для каждого ответа, который проходит 
        через промежуточное программное обеспечение паука в личный Spider. \n
        Возвращает None или возбуждает исключение'''
        return None

    def process_spider_output(self, response, result, spider):
        '''Вызывается с результатами, полученными от Spider после обработки ответа.\n
        Возвращает итерируемые объект Request'''
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        '''Вызывается, когда обработчик загрузки или process_request ()
        (из другого промежуточного программного обеспечения загрузчика) вызывает исключение.'''
        pass

    def process_start_requests(self, start_requests, spider):
        '''Вызывается с запросами запуска паука и работает аналогично методу 
        process_spider_output (), за исключением того, что с ним не связан ответ.
        '''
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        '''Вызывается, когда Spider открывает соединение и готов выполнять запросы'''
        spider.logger.info('Spider opened: %s' % spider.name)


class QuotetutorialDownloaderMiddleware(object):
    '''Описание middleware - логики промежуточных действий между запросами'''

    @classmethod
    def from_crawler(cls, crawler):
        '''Этот метод используется Scrapy для создания личных Spiders.'''
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        '''Вызывается для каждого запроса, который проходит через промежуточное программное обеспечение загрузки.\n
        Вернуть None, чтобы продолжить обрабатывать request
        '''
        return None

    def process_response(self, request, response, spider):
        '''Вызывается с ответом от загрузчика.\n
        Вернуть response - результат запроса'''
        return response

    def process_exception(self, request, exception, spider):
        '''Вызывается, когда обработчик загрузки или process_request ()
        (из другого промежуточного программного обеспечения загрузчика) вызывает исключение.'''
        pass

    def spider_opened(self, spider):
        '''Вызывается, когда Spider открывает соединение и готов выполнять запросы'''
        spider.logger.info('Spider opened: %s' % spider.name)
