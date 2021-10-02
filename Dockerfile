FROM python:3-slim

EXPOSE 8000

WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install -r requirements.txt

COPY . /code/
