#!/usr/bin/env python3
"""
A simple user authentication application built in python and postgresql
"""
import os

from flask import Flask
from config import Config
from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

# csrf = CSRFProtect()


def create_app(config_class=Config):
    """ Application definition and setup
    create_app will contain the app together with all its components. Exported and used in the app entry point
    """
    app = Flask(__name__)
    CORS(app)
    # csrf.init_app(app)
    app.config.from_object(Config)
    JWTManager(app)

    from api.Auth import auth
    app.register_blueprint(auth)

    return app
