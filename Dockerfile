FROM tiangolo/uwsgi-nginx-flask:python3.6

MAINTAINER scurss scurss@gmail.com
WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt



