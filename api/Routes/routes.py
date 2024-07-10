#!/usr/bin/env python3
""" application endpoints """
from flask import request, jsonify, g
from api.Models.tables import User, Organisation
from api.Routes import app
from api.Models import storage


@app.routes('/users/<userId>', methods=['GET'])
def get_user(userId):
    pass