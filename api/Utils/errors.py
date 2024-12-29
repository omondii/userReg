#!/usr/bin/env python3
"""
Custom application error handlers
404 - Not Found
200 - Success
401 - Bad Request
403 - Access denied

201 - Created
"""
import json
from flask import jsonify
from werkzeug.exceptions import HTTPException


def handle_exception(e):
    """ Format http errors to JSON """
    if isinstance(e, HTTPException):
        response = e.get_response()
        error_data = {
            "statusCode": e.code,
            "status": e.name,
            "message": e.description
        }
        return jsonify(error_data), e.code
    # If it's not an HTTPException, return a generic 500 error