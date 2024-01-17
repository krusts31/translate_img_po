FROM alpine:3.18.0 as base
LABEL maintainer=unvlot
RUN apk update && apk upgrade
RUN apk add python3 py3-pip --no-cache && ln -sf python3 /usr/bin/python
RUn apk add tesseract-ocr-data-nld --no-cache
RUN pip install --no-cache --upgrade pip setuptools
COPY ./requirements.txt ./requirements.txt
COPY ./app.py ./app.py
#COPY ./img/ ./img/
COPY ./po/ ./po/
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
