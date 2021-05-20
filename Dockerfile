FROM python:3.9.2

WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN pip install -r requirements.txt --no-cache-dir

ENV FLASK_APP=app

CMD gunicorn -w 4 -b 0.0.0.0:8080 "shortener:create_app()"