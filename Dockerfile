FROM python:3.7-alpine

WORKDIR /app
COPY . /app
RUN pip3 install -r /app/requirements.txt
