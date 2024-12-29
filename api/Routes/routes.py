x#!/usr/bin/env python3
""" application endpoints """
import os
from flask import request, jsonify
from api.Models.tables import User, Organisation
from api.Routes import api
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from api.Models import storage
import uuid
from flasgger import swag_from


@api.route('/user/<userId>', methods=['GET'])
@jwt_required()
@swag_from('../specs/get_user.yml')
def get_user(userId):
    """
    [GET] /api/users/:id : a user gets their own record or user
    record in organisations they belong to or created [PROTECTED].
    :param userId: Logged-in users' id
    current_userId = get_jwt_identity()
    """
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
        "data": data,
        "statusCode": 200
    }), 200


@api.route('/users/all/', methods=['GET'])
@jwt_required()
@swag_from('../specs/get_allusers.yml')
def get_users():
    """
    Gives the full list of all registered users
    :return: data
    """
    users = storage.all(User)
    if not users:
        return jsonify({
            "status": "Not Found",
            "message": "No Data Found",
            "statusCode": 404
        }), 404

    user_list = []
    for user in users.values():
        user_list.append({
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
        })
    return jsonify({
        "status": "success",
        "message": "Data Retrieved",
        "statusCode": 200,
        "data": user_list
    }), 200


@api.route('/organisations', methods=['GET'])
@jwt_required()
@swag_from('../specs/get_allOrgs.yml')
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
        # print(f"User Object: {user}")
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


@api.route('/organisation/<orgId>', methods=['GET'])
@jwt_required()
@swag_from('../specs/get_org.yml')
def get_org(orgId):
    """
    @get_org: the logged-in user gets a single organisation record
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


@api.route('/organisation', methods=['POST'])
@jwt_required()
@swag_from('../specs/create_org.yml')
def create_org():
    """
    [POST] /api/organisations : a logged-in user can create their own new organisation
    :return:
    """
    current_userId = get_jwt_identity()
    user = storage.get(User, current_userId)
    if user is None:
        print('Error')

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    if request.method == 'POST':
        try:
            name = data.get('name')
            description = data.get('description')

            if not all([name, description]):
                return jsonify({
                    "status": "Missing required param",
                    "message": "Bad request",
                    "statusCode": 400
                }), 400

            # Duplicate data checker
            existing_org = storage.get_by_orgname(Organisation, name)
            if existing_org:
                return jsonify({
                    "status": "Bad Request",
                    "message": "Similar Organisation exists",
                    "statusCode": 400
                }), 400

            # Create an Organisation instance and save it to db
            org = Organisation(
                orgId=str(uuid.uuid4()),
                name=name,
                description=description
            )
            storage.new(org)
            storage.save()

            user.organisations.append(org)
            return jsonify({
                "status": "success",
                "message": "Organisation Created succesfully",
                "statusCode": 201
            }), 201

        except Exception as e:
            storage.rollback()
            return jsonify({
                "status": "Bad Request",
                "message": {e},
                "statusCode": 400
            }), 400
    return jsonify({
        "status": "Bad request",
        "message": "Invalid request",
        "statusCode": 401
    }), 401

