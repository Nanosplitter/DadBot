from peewee import Model, CharField, CompositeKey
from services.db_service import get_db

class ServerSettings(Model):
    server_id = CharField()
    server_name = CharField()
    setting_name = CharField()
    setting_value = CharField()

    class Meta:
        primary_key = CompositeKey('server_id', 'setting_name')
        database = get_db()

ServerSettings.create_table(safe=True)
