FROM python:3.6

COPY . /src

RUN pip install /src

RUN mkdir /config

WORKDIR /config

