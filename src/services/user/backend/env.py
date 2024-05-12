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

RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

ADMIN_SERVER_QUEUE = os.getenv("ADMIN_SERVER_QUEUE")
ADMIN_CLIENT_QUEUE = os.getenv("ADMIN_CLIENT_QUEUE")
