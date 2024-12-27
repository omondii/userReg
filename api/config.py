#!/usr/bin/env python3
"""
Contains app configuration class
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SWAGGER = {
        'title': 'User Registration System',
        'version': '0.1',
        'description': 'User Login Management',
        'specs_route': '/docs/'
    }