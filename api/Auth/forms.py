#!/usr/bin/env python3
"""
Application data capture forms
RegistrationForm -
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from api.Models import storage
from api.Models.tables import User, Organisation


class RegistrationForm(FlaskForm):
    """ User registration form. Submits new users to the /register view """
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    phone = StringField("Phone")
    submit = SubmitField('Register')

    """
    def validate_user(self, userId):
        Method to validate user
        user = storage.get(User, userId=userId)
        if user:
            raise ValidationError('') """

    """
    def validate_email(self, email):
        Method to check if email exists
    user = storage.get_by_email(User, email.data)
    if user:
        raise ValidationError("Email already exists")"""