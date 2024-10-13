FROM python:3.12
LABEL authors="masha"

ENV PYTHONUNBUFFERED 1

RUN mkdir /AlfaBilling

WORKDIR /AlfaBilling

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
