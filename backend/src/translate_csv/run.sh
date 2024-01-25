#!/bin/bash
docker build -t test-csv --target dev . &&\
docker run -e TARGET_LANGUAGE=lt \
-e SOURCE_LANGUAGE=lv \
-v ./src:/app/src:delegated \
-v ./dest:/app/dest:delegated \
-it test-csv /bin/sh
