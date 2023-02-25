# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# define build args
ARG PORT
ENV PORT=${PORT}

# project level
WORKDIR /
# copy data folder
COPY ./src/data ./data
COPY ./src/middleware /src

WORKDIR /src
RUN pip install -e .
RUN python3 -m spacy download en_core_web_sm

# directory of fastapi script
WORKDIR /src/middleware/data_retrieval

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT