import peewee

from .AppProperties import AppProperties

class Injector:
    def __init__(self):
        super().__init__()
        self.__properties: AppProperties = AppProperties("app-conf.json")
        self.__db: peewee.SqliteDatabase = peewee.SqliteDatabase("app-data.db")

    def get_properties(self) -> AppProperties:
        return self.__properties

    def get_db(self) -> peewee.SqliteDatabase:
        return self.__db
