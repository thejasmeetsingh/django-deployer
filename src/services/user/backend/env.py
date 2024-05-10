"""
Centralize point to access env variables
"""

import os


SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")
