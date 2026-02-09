# syntax=docker/dockerfile:1

FROM python:3.8-bullseye

# define build args
ARG PORT
ARG SSH_HOST
ARG SSH_PASSWD
ENV PORT=${PORT}

# update
RUN apt-get update

# project level
WORKDIR /
# copy data folder
COPY ./src/data ./data
# COPY ./data/pytorch_model.bin ./data/generator-model/

# copy code
COPY ./src/middleware /src

WORKDIR /src
RUN pip install -U pip==23.0.1 setuptools==67.5.0 wheel==0.40.0
RUN pip install -U spacy==3.5.1
RUN python -m spacy download en_core_web_sm
RUN pip install .

# directory of fastapi script
WORKDIR /src/middleware/tweet_generation

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT