#!/usr/bin/env python3
"""
Contains app configuration class
"""
import os
from dotenv import load_dotenv
from logging.config import dictConfig

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

    @staticmethod
    def logging(logDir):
        """Logging configuration using dictConfig
        @logDir: The log file path
        """
        if not os.path.exists(logDir):
            os.makedirs(logDir)

        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
                },
                'console': {
                    'format': '[%(asctime)s] %(levelname)s %(message)s',
                },
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(logDir, 'app.log'),
                    'maxBytes': 10_000_000,
                    'backupCount': 5,
                    'level': 'DEBUG',
                    'formatter': 'default',
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stderr',
                    'level': 'ERROR',
                    'formatter': 'console',
                },
            },
            'loggers': {
                'app': { 
                    'level': 'DEBUG',
                    'handlers': ['file', 'console'],
                    'propagate': False,
                },
            },
        })