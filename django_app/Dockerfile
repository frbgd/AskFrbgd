FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD python3 manage.py migrate && gunicorn Ask_Frbgd.wsgi:application -c Ask_Frbgd/gunicorn.conf.py
