#!/usr/bin/env python3
""" Endpoints for authorization """
import uuid

from flask import request, jsonify
from api.Auth import auth
from api.Models import storage
from api.Auth.forms import RegistrationForm
from api.Models.tables import User, Organisation
from flask_jwt_extended import (create_access_token,
                                unset_jwt_cookies, get_jwt, get_jwt_identity, jwt_required)
from werkzeug.security import generate_password_hash, check_password_hash
# from api.app import csrf


@auth.route('/register', methods=['POST'])
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
                return jsonify({
                    "status": "Bad request",
                    "message": "All fields are required",
                    "statusCode": 400
                }), 400

            # Check for duplicate data in db
            existing_user = storage.session.query(User).filter(
                (User.email == email) | (User.phone == phone)).first()
            if existing_user:
                return jsonify({
                    "status": "Bad request",
                    "message": "Email or phone number already exists",
                    "statusCode": 400
                }), 400

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
            storage.save()

            # Create an access token for the new user
            access_token = create_access_token(identity=user.userId)

            return jsonify({
                "status": "success",
                "message": "Registration successful",
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
            return jsonify({
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
                "errors": [{
                    "field": "general",
                    "message": str(e)
                }]
            }), 400
    return jsonify({
        "status": "Bad request",
        "message": "Invalid request",
        "statusCode": 400
    }), 400


@auth.route('/login', methods=['POST'])
def login():
    """ Logs a user based on provided details """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate the input data
    if not all([email, password]):
        return jsonify({
            "status": "Bad request",
            "message": "Email and password are required",
            "statusCode": 400
        }), 400

    # Retrieve the user by email
    user = storage.get_by_email(User, email)

    if user and check_password_hash(user.password, password):
        # Create a new access token
        access_token = create_access_token(identity=user.userId)

        response = {
            "status": "success",
            "message": "Login successful",
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
        }
        return jsonify(response), 200
    else:
        response = {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }
        return jsonify(response), 401
