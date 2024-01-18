FROM alpine:3.18.0 as base
LABEL maintainer=01gr0und5
WORKDIR /var/www/backend

RUN apk update && apk upgrade
RUN apk add python3 py3-pip tesseract-ocr-data-nld --no-cache && ln -sf python3 /usr/bin/python
RUN pip install --no-cache --upgrade pip setuptools
COPY ./requirements.txt ./requirements.txt
COPY ./ ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Development image
FROM base as dev
COPY ./src ./src
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT --reload"]

# Testing image
FROM base as test
COPY ./requirements-test.txt ./requirements-test.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements-test.txt
COPY ./src ./src
CMD ["pytest", "./src"]

# Production image
FROM base as prod
COPY ./src ./src
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]
