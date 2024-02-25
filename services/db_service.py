from peewee import MySQLDatabase
from pymysql import OperationalError
import yaml

# Load your configuration
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class ReconnectMySQLDatabase(MySQLDatabase):
    def execute_sql(self, sql, params=None, commit=True):
        try:
            return super().execute_sql(sql, params, commit)
        except OperationalError as e:
            print(f"An OperationalError occurred: {e}")
            if e.args[0] in (
                2006,
                2013,
            ):
                print(
                    "Database connection lost, attempting to reconnect and retry the query."
                )
                self.connect(reuse_if_open=True)
                return super().execute_sql(sql, params, commit)
            else:
                raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


def get_db():
    return ReconnectMySQLDatabase(
        config["databasename"],
        user=config["dbuser"],
        password=config["dbpassword"],
        host=config["dbhost"],
        port=3306,
    )
