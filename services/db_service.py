from peewee import MySQLDatabase
import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class ReconnectMySQLDatabase(MySQLDatabase):
    def execute_sql(self, sql, params=None, commit=True):
        try:
            return super().execute_sql(sql, params, commit)
        except Exception as e:
            print(
                "Database connection lost, attempting to reconnect and retry the query."
            )
            self.connect(reuse_if_open=True)
            return super().execute_sql(sql, params, commit)


def get_db():
    return ReconnectMySQLDatabase(
        config["databasename"],
        user=config["dbuser"],
        password=config["dbpassword"],
        host=config["dbhost"],
        port=3306,
    )
