import datetime
import uuid
import json

import peewee


class DomainObject(peewee.Model):
    _last_modified_ts = peewee.DateTimeField(default=datetime.datetime.utcnow)
    _creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        from main import INJECTOR
        database = INJECTOR.get_db()


class Organization(DomainObject):
    name = peewee.TextField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)


class CollectedDataByOrganization(DomainObject):
    collection_id = peewee.UUIDField(default=uuid.uuid4)
    url = peewee.TextField()
    resources = peewee.BigBitField()


class OrganizationProcessing(DomainObject):
    organization = peewee.ForeignKeyField(Organization, backref="organization")
    collected_data = peewee.ForeignKeyField(CollectedDataByOrganization, backref="collected_data")


def validate_database(db_instance):
    db_instance.create_tables([Organization, OrganizationProcessing, CollectedDataByOrganization])