FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y gdal-bin libgdal-dev

RUN pip install -r requirements.txt

EXPOSE 5000
