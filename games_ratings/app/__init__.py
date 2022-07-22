import os

from flask import Flask

from .routes import bp
from .db import mongo
from .errors import register_errors

def create_app()-> Flask:
    app = Flask(__name__)
    db_host=os.environ.get('DB_HOST')
    db_name= os.environ.get('MONGO_INITDB_DATABASE')
    db_username= os.environ.get('MONGO_INITDB_ROOT_USERNAME')
    db_password= os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

    app.config["MONGO_URI"] = f"mongodb://{db_username}:{db_password}@{db_host}:27017/{db_name}?authSource=admin"
    
    mongo.init_app(app)

    app.register_blueprint(bp)

    register_errors(app)

    return app