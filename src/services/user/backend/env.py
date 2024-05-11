"""
Centralize point to access env variables
"""

import os


SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB_NAME = os.getenv("REDIS_DB_NAME")
