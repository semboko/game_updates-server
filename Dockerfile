FROM python:3.12.1-slim-bullseye

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

RUN apt -y update && \
    apt -y upgrade && \
    apt -y install libpq-dev gcc && \
    pip3 install -r requirements.txt

COPY . .