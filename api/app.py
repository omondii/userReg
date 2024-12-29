#!/usr/bin/env python3
"""
A simple user authentication application built in python and postgresql
"""
from flask import Flask
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from Models.engine.db_storage import DBStorage
from flasgger import Swagger
import os


def create_app(config_class=Config, db_engine=None):
    """ Application definition and setup
    create_app will contain the app together with all its components. Exported and used in the app entry point
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    JWTManager(app)
    Swagger(app)

    # Initialize db storage
    app.db_storage = DBStorage(db_engine=db_engine)
    app.db_storage.reload()

    from Auth import auth
    app.register_blueprint(auth)

    from Routes import api
    app.register_blueprint(api)

    return app

app = create_app()

