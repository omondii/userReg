#!/usr/bin/env python3
""" application endpoints """
from flask import request, jsonify, g
from api.Models.tables import User, Organisation
from api.Routes import api
from flask_jwt_extended import (create_access_token,
                                unset_jwt_cookies, get_jwt, get_jwt_identity, jwt_required)
from api.Models import storage


@api.route('/users/all/', methods=['GET'])
@jwt_required()
def all_users():
    """
    Gives the full list of all registered users
    :return: data
    """
    users = storage.all(User).values()
    if not users:
        return jsonify({
            "status": "Not Found",
            "Message": "No Data Found",
            "statusCode": 404
        }), 404

    user_list = []
    for user in users:
        user_list.append({
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
        })
    return jsonify({
        "status": "success",
        "Message": "Data Retrieved",
        "data": user_list
    }), 200


@api.route('/users/<userId>', methods=['GET'])
@jwt_required()
def get_user(userId):
    """
        [GET] /api/users/:id : a user gets their own record or user
        record in organisations they belong to or created [PROTECTED].
    :param userId: Logged-in users' id
    :return:
    """
    current_userId = get_jwt_identity()

    if userId != current_userId:
        print(current_userId)
        return jsonify({
            "status": "Bad Request",
            "message": "Invalid Id",
            "statusCode": 401
        }), 401

    user = storage.get(User, userId)
    if not user:
        return jsonify({
            "status": "Bad Request",
            "message": "User Not Found",
            "statusCode": 404
        }), 404

    data = {
        "userId": user.userId,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "phone": user.phone
    }
    return jsonify({
        "status": "success",
        "message": "User record retrieved",
        "data": data
    }), 200


@api.route('/organisations', methods=['GET'])
@jwt_required()
def get_orgs():
    """
    [GET] /api/organisations : gets all your organisations the user
    belongs to or created. If a user is logged in properly, they can get all their organisations
    :return: List of all current_user orgs
    """
    current_userId = get_jwt_identity()
    print(f"Current User Id: {current_userId}")

    try:
        user = storage.get('User', current_userId)
        print(f"User Object: {user}")
        if not user:
            return jsonify({
                "status": "Error",
                "message": "User Not Found",
                "statusCode": 404
            }), 404

        orgs = user.organisations
        print(f"User's Orgs: {orgs}")

        org_data = [{
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
        } for org in orgs]

        return jsonify({
            "status": "success",
            "message": "All user organisations returned successfully",
            "data": org_data
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "Error",
            "message": f"An error occurred: {str(e)}",
            "statCode": 500
        }), 500


@api.route('/organisations/<orgId>', methods=['GET'])
@jwt_required()
def get_org(orgId):
    """
    [GET] /api/organisations/:orgId the logged-in user gets a single organisation record
    :param orgId: organisation id to retrieve
    :return: payload containing the org data
    """
    current_userId = get_jwt_identity()

    org = storage.get('Organisation', orgId)
    if not org:
        return jsonify({
            "status": "fail",
            "message": "Organization not found"
        }), 404

    user = storage.get('User', current_userId)
    if not user:
        return jsonify({
            "status": "fail",
            "message": "User not found",
        }), 404

    if org not in user.organisations:
        return jsonify({
            "status": "fail",
            "message": "Access denied"
        }), 403

    org_data = {
        "organisations": [
            {
                "orgId": org.orgId,
                "name": org.name,
                "description": org.description,
            }
        ]
    }
    return jsonify ({
        "status": "success",
        "message": "Organisations retrieved successfully",
        "data": org_data
    }), 200


@api.route('/organisations', methods=['POST'])
@jwt_required()
def create_org():
    """
    [POST] /api/organisations : a user can create their new organisation
    :return:
    """
    data = request.get_json()
    name = data.get('email')
    description = data.get('description')