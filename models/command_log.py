from services.db_service import get_db
import datetime
from peewee import Model, CharField, DateTimeField, AutoField


class CommandLog(Model):
    id = AutoField()
    server_id = CharField(null=True)  # Null for DMs
    server_name = CharField(null=True)  # Null for DMs
    user_id = CharField()
    user_name = CharField()
    command_name = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = get_db()

    def __str__(self):
        server_str = f"Server: {self.server_name} ({self.server_id})" if self.server_id else "DM"
        return f"{server_str}, User: {self.user_name} ({self.user_id}), Command: {self.command_name}, Time: {self.timestamp}"

    def __repr__(self):
        return self.__str__()


# Create the table if it doesn't exist
CommandLog.create_table(safe=True)