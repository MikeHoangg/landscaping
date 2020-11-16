FROM python:3.8 as base

ENV PYTHONUNBUFFERED=0

WORKDIR /landscaping

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM base as test
RUN pip install coverage
COPY ./ ./

FROM base
COPY ./ ./
