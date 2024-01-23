FROM alpine:3.18.0 as base

LABEL maintainer=01gr0und5

WORKDIR /app

RUN apk update && apk upgrade

RUN apk add python3 py3-pip --no-cache &&\
	ln -sf python3 /usr/bin/python

RUN pip install --no-cache --upgrade pip setuptools
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Development image
FROM base as dev
RUN apk add --no-cache vim 
RUN pip install --no-cache-dir --upgrade -r ./requirements-test.txt
COPY ./translate_po.py ./translate_po.py
CMD ["python", "translate_po.py"]

# Testing image
FROM dev as test
CMD ["pytest", "./src"]

# Production image
FROM base as prod
COPY ./translate_po.py ./translate_po.py
CMD ["python", "translate_po.py"]
