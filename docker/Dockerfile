FROM python:3.7-slim as base
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /code

FROM base as dev

FROM base as build
COPY ./ /code
