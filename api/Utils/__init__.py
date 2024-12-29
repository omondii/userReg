#!/usr/bin/env python3
"""
Utility Package
Error blueprint definition

"""
from flask import Blueprint

errors = Blueprint('errors', __name__)

from . import errors
