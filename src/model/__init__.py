import datetime
import uuid
import json

import peewee


class DomainObject(peewee.Model):
    '''Суперкласс объекдиняющий все классы доменной модели\n
    DomainObject расширяет peewee.Model\n
    _last_modified_ts: DateTimeField - поле, хранит временную метку, когда запись была последний раз обновлена\n
    _creation_date: DateTimeField - поле, хранит временную метку, когда запись была создана'''
    _last_modified_ts = peewee.DateTimeField(default=datetime.datetime.utcnow)
    _creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        '''Метакласс, содержит информацию к какой БД подключаться'''
        from main import INJECTOR
        database = INJECTOR.get_db()


class Organization(DomainObject):
    '''Organization. Доменный класс. \n
    name: TextField - поле, хранит название организации - сайта\n
    creation_date: DateTimeField - поле, хранит дату создания организации'''
    name = peewee.TextField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)


class CollectedDataByOrganization(DomainObject):
    '''CollectedDataByOrganization. Доменный класс.\n
    collection_id: UUIDField - суррогатный ключ\n
    url: TextField - текстовое поле для хранения URL организации-сайта\n
    resources: BigBitField - байтовое поле, для хранения больших данных'''
    collection_id = peewee.UUIDField(default=uuid.uuid4)
    url = peewee.TextField()
    resources = peewee.BigBitField()


class OrganizationProcessing(DomainObject):
    '''OrganizationProcessing. Доменный класс\n
    organization: ForeignKeyField - ссылка на Organization\n
    collected_data: ForeignKeyField - ссылка на CollectedDataByOrganization'''
    organization = peewee.ForeignKeyField(Organization, backref="organization")
    collected_data = peewee.ForeignKeyField(
        CollectedDataByOrganization, backref="collected_data")


def validate_database(db_instance):
    '''Валидация базы данных.\n
    В случае её отсутствия - создается база данных app-data.db
    '''
    db_instance.create_tables(
        [Organization, OrganizationProcessing, CollectedDataByOrganization])
