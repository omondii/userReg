#!/usr/bin/env python3
""" Authentication and Authorization Module """
from flask import Blueprint
import logging

auth = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger('app')

from . import routes
