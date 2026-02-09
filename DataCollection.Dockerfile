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
RUN pip install -U pip==23.0.1 setuptools==67.5.0 wheel==0.40.0
RUN pip install -U spacy==3.5.1
RUN curl -I https://google.com
RUN python -m spacy download en_core_web_sm
RUN pip install -e .

# directory of fastapi script
WORKDIR /src/middleware/data_collection

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT