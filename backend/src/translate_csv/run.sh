#!/bin/bash
docker build -t test-csv --target dev . &&\
docker run -e TARGET_LANGUAGE=$1 \
-e SOURCE_LANGUAGE=$2 \
-v ./src:/app/src:delegated \
-v ./dest:/app/dest:delegated \
-it $3 test-csv $4
