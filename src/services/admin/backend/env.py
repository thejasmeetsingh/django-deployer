"""
Centralize point to access env variables
"""

import os

SECRET_KEY = os.getenv("SECRET_KEY")

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_DB_HOST")

PORT = os.getenv("PORT")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
SERVER_QUEUE = os.getenv("SERVER_QUEUE")
CLIENT_QUEUE = os.getenv("CLIENT_QUEUE")

ACCESS_TOKEN_EXP_MINUTES = os.getenv("ACCESS_TOKEN_EXP_MINUTES")
REFRESH_TOKEN_EXP_MINUTES = os.getenv("REFRESH_TOKEN_EXP_MINUTES")

# [{"email": "admin@example.com", "password": "hashed_password"}]
ADMIN_CREDENTIALS = os.getenv("ADMIN_CREDENTIALS")
