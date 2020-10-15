FROM python:latest

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN pip install Flask PyYAML

EXPOSE 5000