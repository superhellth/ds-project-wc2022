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
RUN pip install -e .

# directory of fastapi script
WORKDIR /src/middleware/data_collection

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT