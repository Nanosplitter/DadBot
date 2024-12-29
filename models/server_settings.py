from peewee import Model, CharField, SqliteDatabase

db = SqliteDatabase('my_database.db')

class ServerSettings(Model):
    server_id = CharField()
    setting_name = CharField()
    setting_value = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([ServerSettings], safe=True)
