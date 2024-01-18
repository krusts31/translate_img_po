#!/bin/sh
(npm run start&)
nginx -g "daemon off;"
