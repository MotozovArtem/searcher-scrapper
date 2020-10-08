import peewee


class Injector:
    def __init__(self):
        super().__init__()
        self.__db: peewee.SqliteDatabase = peewee.SqliteDatabase("app-data.db")

    def get_db(self) -> peewee.SqliteDatabase:
        return self.__db
