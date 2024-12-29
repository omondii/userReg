#!/usr/bin/env python3
""" JWT token creator """
from flask_jwt_extended import create_access_token
from datetime import timedelta


def generate_token(user_id):
    """
    Generates a jwt token and sets its expiry period
    :param user_id: User identity
    :return: access_token
    """
    access_token = create_access_token(identity=user_id,
                                       expires_delta=timedelta(hours=1))
    return access_token
