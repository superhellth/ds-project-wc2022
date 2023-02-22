# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# project level
WORKDIR /
# copy data folder
COPY ./src/data ./data
COPY ./src/middleware /src

WORKDIR /src
RUN pip install pytorch-lightning==1.7.7 fastapi[all] aitextgen uvicorn elasticsearch==7.17

# directory of fastapi script
WORKDIR /src/middleware/tweet_generation

CMD [ "python3", "-m" , "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]