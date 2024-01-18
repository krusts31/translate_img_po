#!/bin/bash

# Start the containers using Docker Compose
docker compose -f docker-compose-test.yaml --env-file .env-test up --build -d

# Container names as defined in your docker-compose.yml
CONTAINER_1="python-docker-fronend"
CONTAINER_2="python-docker-backend"
RUNING_CONTAINER_COUNT=2

BACKEND_CONTAINERS_ID=$(docker compose -f docker-compose-test.yaml --env-file .env-test ps -q backend)

FRONTEND_CONTAINERS_ID=$(docker compose -f docker-compose-test.yaml --env-file .env-test ps -q frontend)

while [ $RUNING_CONTAINER_COUNT -ne 0 ]
do
	RUNING_CONTAINER_COUNT=$(docker compose -f docker-compose-test.yaml --env-file .env-test ps -q | wc -l)
	EXIT_STATUS_BACKEND=$(docker inspect $BACKEND_CONTAINERS_ID -f '{{.State.ExitCode}}')
	EXIT_STATUS_FRONTEND=$(docker inspect $FRONTEND_CONTAINERS_ID -f '{{.State.ExitCode}}')
	echo exit status frontend: $EXIT_STATUS_FRONTEND backend: $EXIT_STATUS_BACKEND
	if [ $EXIT_STATUS_BACKEND -ne 0 ] || [ $EXIT_STATUS_FRONTEND -ne 0 ]
	then
		echo "TEST FAILED"
		exit 1
	fi
	sleep 1
done

echo "TEST PASS"
exit 0
