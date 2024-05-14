# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# define build args
ARG PORT
ENV PORT=${PORT}

# project level
WORKDIR /

# copy code
COPY . ./src

WORKDIR /src
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install -e .

# directory of fastapi script
WORKDIR /src/middleware/data_collection

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT