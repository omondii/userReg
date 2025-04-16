#!/usr/bin/env python3
""" Routes Module: Contains business logic views """
from flask import Blueprint
import logging

api = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger('app')

from . import routes
