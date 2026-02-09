# syntax=docker/dockerfile:1

FROM python:3.8-bullseye

# define build args
ARG PORT
ENV PORT=${PORT}

RUN apt-get update

# project level
WORKDIR /

# copy code
COPY . ./src

WORKDIR /src
RUN pip install -U pip==25.0.1 setuptools==67.5.0 wheel==0.40.0
COPY en_core_web_sm-3.5.0-py3-none-any.whl .
RUN pip install ./en_core_web_sm-3.5.0-py3-none-any.whl
RUN pip install -U spacy==3.5.1
RUN python -m spacy download en_core_web_sm
RUN pip install -e .

# directory of fastapi script
WORKDIR /src/middleware/data_collection

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT