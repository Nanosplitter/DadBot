from peewee import *
import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


def get_db():
    return MySQLDatabase(config["databasename"], user=config["dbuser"], password=config["dbpassword"], host=config["dbhost"], port=3306)

