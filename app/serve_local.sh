#!/bin/sh
APP_HOST_NAME=0.0.0.0
APP_MODULE=rest_apiserver
APP_THREADS=2
APP_PORT=8000
python -m ${APP_MODULE}:app