FROM python:3.6

RUN apt-get update && apt-get install -y graphviz

RUN pip install docutils

COPY . /src
RUN pip install /src

RUN mkdir /config

WORKDIR /config

ENTRYPOINT []
