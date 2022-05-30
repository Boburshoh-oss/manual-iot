FROM python:3.8.7-slim-buster

WORKDIR /app


RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

RUN pip3 install --upgrade setuptools
RUN pip install --upgrade pip

RUN  apt-get update \
     && apt-get install -y redis-server 
   

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt


COPY . /app
