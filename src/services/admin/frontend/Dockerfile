FROM node:22-alpine3.18

RUN apk add --no-cache build-base

WORKDIR /usr/app

COPY package*.json /usr/app
RUN npm install

COPY . /usr/app
