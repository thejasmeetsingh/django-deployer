FROM python:3.11-alpine

RUN apk add --no-cache build-base libffi-dev

RUN wget https://releases.hashicorp.com/terraform/1.8.5/terraform_1.8.5_linux_amd64.zip
RUN unzip terraform_1.8.5_linux_amd64.zip && rm terraform_1.8.5_linux_amd64.zip
RUN mv terraform /usr/bin/terraform

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

RUN chmod +x /code/terraform.sh