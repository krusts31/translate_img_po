FROM alpine:3.18.0 as base
LABEL maintainer=01gr0und5
RUN apk update && apk upgrade
RUN apk add python3 py3-pip --no-cache && ln -sf python3 /usr/bin/python
RUn apk add tesseract-ocr-data-nld --no-cache
RUN pip install --no-cache --upgrade pip setuptools
COPY ./requirements.txt ./requirements.txt
COPY ./app.py ./app.py
#COPY ./img/ ./img/
COPY ./po/ ./po/
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

FROM alpine:3.18.0 as base
LABEL maintainer=01gro0nd5
RUN apk update && apk upgrade
RUN apk add python3 py3-pip --no-cache && ln -sf python3 /usr/bin/python
RUN pip install --no-cache --upgrade pip setuptools
RUN apk add --no-cache gcc musl-dev linux-headers python3-dev libffi-dev
WORKDIR /var/www/backend
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Development image
FROM base as dev
COPY ./app ./app
COPY ./weaviate_data ./weaviate_data
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001", "--reload"]

# Testing image
FROM base as test
COPY ./requirements-test.txt ./requirements-test.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements-test.txt
COPY ./app ./app
COPY ./weaviate_data ./weaviate_data
CMD ["pytest", "./app"]

# Production image
FROM base as prod
COPY ./app ./app
COPY ./weaviate_data ./weaviate_data
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001"]
