#!/usr/bin/env python3
"""
Contains app configuration class
"""
import os


class Config:
    SECRET_KEY=os.getenv('SECRET_KEY', '3a1fcf53a8aee5b8d4e3a3c59b3a4b9e')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'fvtneweoifvmwrfiovrv')

