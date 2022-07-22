import os

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('MONGO_INITDB_DATABASE')
DB_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
DB_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
