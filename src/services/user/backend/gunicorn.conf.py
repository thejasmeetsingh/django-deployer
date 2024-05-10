"""
Gunicorn Config
"""

import multiprocessing

import env

bind = f"0.0.0.0:{env.PORT}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2
accesslog = "-"
