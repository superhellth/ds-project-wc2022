# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# define build args
ARG PORT
ARG SSH_HOST
ARG SSH_PASSWD
ENV PORT=${PORT}

# install sshpass
RUN apt-get update && \
    apt-get install -y sshpass

# project level
WORKDIR /
# copy data folder
COPY ./src/data ./data
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/pytorch_model.bin ./data/generator-model

# copy code
COPY ./src/middleware /src

WORKDIR /src
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install .
RUN pip install pytorch-lightning==1.7.7 fastapi[all] aitextgen uvicorn elasticsearch==7.17

# directory of fastapi script
WORKDIR /src/middleware/tweet_generation

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT