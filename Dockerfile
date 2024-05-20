FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

EXPOSE 8000
