# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

WORKDIR /

COPY . .

RUN pip install -e ./

WORKDIR /middleware/data_collection

CMD [ "python3", "-m" , "uvicorn", "main:app", "--host=0.0.0.0"]