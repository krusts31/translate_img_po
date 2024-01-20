#!/bin/sh
$(uvicorn src.main:app --host 0.0.0.0 --port $PORT --log-level critical)&
echo "server started"
ps aux
schemathesis run --wait-for-schema=5 --checks all http://localhost:$PORT/openapi.json --force-schema-version 30
