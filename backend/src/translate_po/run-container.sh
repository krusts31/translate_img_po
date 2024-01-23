#!/bin/bash
docker build -t translate-po-image --target prod . &&\
	docker run -e TARGET_FILE=$1\
		-e TARGET_LANGUAGE=$2\
		-e SOURCE_LANGUAGE=$3\
		-v ./result:/app/result\
		-v ./po-files/:/app/po-files/\
		translate-po-image
