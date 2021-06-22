FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD gunicorn app:app -c wsgi_app.conf.py
