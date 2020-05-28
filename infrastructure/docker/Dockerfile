FROM python:3.7-slim as base
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /code

FROM base as dev
CMD python project/manage.py runserver 0.0.0.0:8000

FROM base as build
COPY ./ /code
CMD python project/manage.py migrate; python project/manage.py runserver 0.0.0.0:8000
