class PropertiesException(Exception):
    '''Исключение настроек приложения'''
    def __init__(self, value):
        '''value: str - сообщение ошибки'''
        self.msg = value

    def __str__(self):
        '''Вызывается при конвертации объекта в строку'''
        return self.msg


class NotSupportedSearcherTypeException(Exception):
    '''Исключение о не поддерживаемом типа информационно-поисковой системы'''
    def __init__(self, value):
        '''value: str - сообщение ошибки'''
        self.msg = value

    def __str__(self):
        '''Вызывается при конвертации объекта в строку'''
        return self.msg
