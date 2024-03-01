from peewee import *
from services.db_service import get_db


class StepLog(Model):
    id = AutoField()
    server_id = CharField()
    user_id = CharField()
    steps = IntegerField()
    submit_time = DateTimeField()

    class Meta:
        database = get_db()

    def __str__(self):
        return f"Server: {self.server_id}, User: {self.user_id}, Steps: {self.steps}, Time: {self.submit_time}"

    def __repr__(self):
        return f"Server: {self.server_id}, User: {self.user_id}, Steps: {self.steps}, Time: {self.submit_time}"
