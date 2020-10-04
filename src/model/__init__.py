import datetime
import uuid
import json

import peewee

class JsonField(peewee.Field):
    field_type="text"

    def db_value(self, value):
        return json.loads(value)

    def python_value(self, value):
        return json.dumps(value)


class DomainObject(peewee.Model):
    _inner_id = peewee.UUIDField(default=uuid.uuid4)
    _last_modified_ts = peewee.DateTimeField(default=datetime.datetime.utcnow)
    _creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        from main import INJECTOR
        database = INJECTOR.get_db()


class Organization(DomainObject):
    name = peewee.TextField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    codes = peewee.TextField()


# class CollectedResource(EmbeddedDocument):
#     resource = TextField(required=True)
#     data = TextField(required=True)


class CollectedDataByOrganization(DomainObject):
    collection_id = peewee.UUIDField(default=uuid.uuid4)
    url = peewee.TextField()
    resources = JsonField()


class OrganizationProcessing(DomainObject):
    organization = peewee.ForeignKeyField(Organization, backref="organization_processing")
    collected_data = peewee.ForeignKeyField(CollectedDataByOrganization, backref="collected_data_processing")
    classified = peewee.TextField()


def validate_database(db_instance):
    db_instance.create_tables([Organization, OrganizationProcessing, CollectedDataByOrganization])