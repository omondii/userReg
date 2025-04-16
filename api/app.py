#!/usr/bin/env python3
"""
A simple user authentication application built in python and postgresql
"""
from flask import Flask
from .config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.Models.engine.db_storage import DBStorage
from flasgger import Swagger
import os
import logging


def create_app(config_class=Config, db_engine=None):
    """ Application definition and setup
    create_app will contain the app together with all its components. Exported and used in the app entry point
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(Config)
    JWTManager(app)
    Swagger(app)

    """ Logging configuration
    Override Flasks default logger, use Config def
    """
    logDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'logs')
    Config.logging(logDir)
    logger = logging.getLogger('app')
    # Logger Test
    logger.info("User Registration System Starting....")

    # Initialize db storage
    app.db_storage = DBStorage(db_engine=db_engine)
    app.db_storage.reload()


    from api.Auth import auth
    app.register_blueprint(auth)

    from api.Routes import api
    app.register_blueprint(api)

    # @app.errorhandler(Exception)
    # def global_error_handler(e):
    #     pass

    return app

