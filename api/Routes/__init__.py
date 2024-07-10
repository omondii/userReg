#!/usr/bin/env python3
""" Initialize api blueprints here """
from flask import Blueprint

app = Blueprint('app', __name__, url_prefix='/api')

from . import routes
