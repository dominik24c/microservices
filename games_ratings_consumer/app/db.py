from pymongo import MongoClient

from . import config

uri_driver = f'mongodb://{config.DB_USERNAME}:{config.DB_PASSWORD}'\
    f'@{config.DB_HOST}:27017/{config.DB_NAME}?authSource=admin'

client = MongoClient(uri_driver)

db = client[config.DB_NAME]
collection = db['game_ratings']
