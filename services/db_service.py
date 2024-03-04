import yaml
from peewee import MySQLDatabase, InterfaceError, OperationalError
import time

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class ReconnectMySQLDatabase(MySQLDatabase):
    max_retries = 3
    retry_delay = 2

    def execute_sql(self, sql, params=None, commit=True):
        for attempt in range(self.max_retries):
            try:
                return super().execute_sql(sql, params, commit)
            except (InterfaceError, OperationalError) as e:
                print(f"Attempt {attempt + 1}: Database connection error - {str(e)}")

                if attempt < self.max_retries - 1:
                    print("Attempting to reconnect and retry the query.")
                    self._reconnect()
                    time.sleep(self.retry_delay)
                else:
                    print("Max reconnection attempts reached. Raising the exception.")
                    raise
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                raise

    def _reconnect(self):
        try:
            self.close()
        except Exception as e:
            print(f"Error closing the database connection: {str(e)}")
        finally:
            self.connect()


def get_db():
    return ReconnectMySQLDatabase(
        config["databasename"],
        user=config["dbuser"],
        password=config["dbpassword"],
        host=config["dbhost"],
        port=config.get("dbport", 3306),
    )
