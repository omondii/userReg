#!/usr/bin/env python3
""" Endpoints for authorization """
import uuid
from flask import request, jsonify, abort
from api.Auth import auth, logger
from api.Models import storage
from api.Auth.utils import generate_token
from api.Models.tables import User, Organisation
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Conflict
from flask_jwt_extended import jwt_required
from flasgger import swag_from


@auth.route('/register', methods=['POST'])
@swag_from('../specs/register_user.yml')
def register():
    """ View to add a new user to db after data validation"""
    data = request.get_json()
    if request.method == 'POST':
        try:
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')

            # Validate the input data
            if not all([firstName, lastName, email, password, phone]):
                logger.info('Failed to register user. Incomplete Details')
                return jsonify({
                    "status": "Bad request",
                    "message": "All fields are required",
                    "statusCode": 400
                }), 400

            # Check for duplicate data in db
            existing_user = storage.get_by_email(User, email)
            if existing_user:
                logger.info(f'Existing user of ID: {User.userId} creation attempt')
                return jsonify({
                    "status": "Conflict",
                    "message": "User Exists!",
                    "statusCode": 409
                }), 409

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new user instance
            user = User(
                userId=str(uuid.uuid4()),
                firstName=firstName,
                lastName=lastName,
                email=email,
                password=hashed_password,
                phone=phone
            )

            # Create a new organisation instance
            org_name = f"{firstName}'s Organisation"
            organisation = Organisation(
                orgId=str(uuid.uuid4()),
                name=org_name,
                description=f"Organisation for {firstName} {lastName}"
            )

            # Add user and organisation to the session and commit
            storage.new(user)
            storage.new(organisation)
            logger.info(f'User: {user.userId} of Organization: {organisation.name} Created')

            # create association table
            user.organisations.append(organisation)

            storage.save()

            access_token = generate_token(user.userId)

            return jsonify({
                "status": "success",
                "message": "Registration successful",
                "statusCode": 201,
                "data": {
                    "accessToken": access_token,
                    "user": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone
                    }
                }
            }), 201
        except Exception as e:
            storage.rollback()
            logger.debug(f'Error: {str(e)}')
            return jsonify({
                "status": "Bad request",
                "message": {str(e)},
                "statusCode": 400
            }), 400
    return jsonify({
        "status": "Bad request",
        "message": "Invalid request",
        "statusCode": 401
    }), 401


@auth.route('/login', methods=['POST'])
@swag_from('../specs/login_user.yml')
def login():
    """ Logs a user based on provided details """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate the input data
    if not all([email, password]):
        return jsonify({
            "status": "Bad request",
            "message": "Missing required filed/s",
            "statusCode": 400
        }), 400

    # Retrieve the user by email
    user = storage.get_by_email(User, email)

    if user and check_password_hash(user.password, password):
        # Create a new access token
        access_token = generate_token(user.userId)
        logger.debug(f'User: {user.userId} Logged In succesfully')

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "statusCode": 200,
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone
                }
            }
        }), 200
    else:
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }), 401

@auth.route('/logout', methods=['POST'])
@jwt_required()
@swag_from('../specs/logout.yml')
def logout():
    pass

