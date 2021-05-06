import peewee


class Injector:
    '''
    Класс, реализующий паттерн Dependency Injection
    Создает, аккумулирует и закрывает все Singleton сущности приложения 
    '''
    def __init__(self):
        '''
        Создает все Singleton сущности приложения
        '''
        super().__init__()
        self.__db: peewee.SqliteDatabase = peewee.SqliteDatabase("app-data.db")

    def get_db(self) -> peewee.SqliteDatabase:
        '''
        Получить ссылку на объект базы данных
        '''
        return self.__db
