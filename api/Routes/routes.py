#!/usr/bin/env python3
""" application endpoints """
from flask import request, jsonify, g
from api.Models.tables import User, Organisation
from api.Routes import app
from api.Models import storage
from flask_jwt_extended import (create_access_token,
                                unset_jwt_cookies, get_jwt, get_jwt_identity, jwt_required)
from api.Models import storage


@app.routes('/users/<userId>', methods=['GET'])
@jwt_required()
def get_user(userId):
    """
        [GET] /api/users/:id : a user gets their own record or user
        record in organisations they belong to or created [PROTECTED].
    :param userId: Loged in users id
    :return:
    """
    pass
