FROM python:3.10.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /uzbbcbot

WORKDIR /uzbbcbot
COPY requirements.txt /uzbbcbot/

RUN pip install --no-cache-dir -r requirements.txt && apt update

COPY . /uzbbcbot/
