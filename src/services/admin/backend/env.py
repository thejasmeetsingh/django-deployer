import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

PORT = os.getenv("PORT")
GRPC_PORT = os.getenv("GRPC_PORT")

ACCESS_TOKEN_EXP_MINUTES = os.getenv("ACCESS_TOKEN_EXP_MINUTES")
REFRESH_TOKEN_EXP_MINUTES = os.getenv("REFRESH_TOKEN_EXP_MINUTES")