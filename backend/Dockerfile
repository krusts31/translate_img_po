FROM alpine:3.18.0 as base
LABEL maintainer=01gr0und5
WORKDIR /var/www/backend

RUN apk update && apk upgrade
RUN apk add python3 py3-pip tesseract-ocr-data-nld --no-cache && ln -sf python3 /usr/bin/python
RUN pip install --no-cache --upgrade pip setuptools
COPY ./ ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Development image
FROM base as dev
RUN apk add --no-cache vim 
RUN pip install --no-cache-dir --upgrade -r ./requirements-test.txt
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT --reload"]

# Testing image
FROM dev as test
CMD ["pytest", "./src"]

# Testing image
FROM dev as end-to-end-test
CMD ["sh", "./end-to-end-test.sh"]

# Production image
FROM base as prod
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]
