from peewee import Model, CharField, BooleanField, CompositeKey, SqliteDatabase
from services.db_service import get_db

class ServerSettings(Model):
    server_id = CharField()
    setting_name = CharField()
    setting_value = BooleanField()

    class Meta:
        primary_key = CompositeKey('server_id', 'setting_name')
        database = get_db()

ServerSettings.create_table(safe=True)
