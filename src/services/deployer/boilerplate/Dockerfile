FROM python:3.11-alpine

RUN apk add --no-cache build-base libffi-dev postgresql-dev
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /code/