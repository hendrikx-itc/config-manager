FROM python:3.6

COPY . /src

RUN pip install /src

ENTRYPOINT ["render-config"]
