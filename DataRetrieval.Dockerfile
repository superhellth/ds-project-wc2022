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
# copy data directory
COPY ./src/data ./data
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/collocations2.json ./data
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/collocations3.json ./data
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/collocations4.json ./data

WORKDIR /data
RUN mkdir word-embeddings
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/w2v_epochs=100.emb ./word-embeddings
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/w2v_epochs=100.emb.syn1neg.npy ./word-embeddings
RUN sshpass -p ${SSH_PASSWD} scp -o StrictHostKeyChecking=no ${SSH_HOST}:/home/data/w2v_epochs=100.emb.wv.vectors.npy ./word-embeddings

# copy code
COPY ./src/middleware /src

WORKDIR /src
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install -e .

# directory of fastapi script
WORKDIR /src/middleware/data_retrieval

CMD python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT