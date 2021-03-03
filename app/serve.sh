#!/bin/sh

echo "Running inside serve.sh:"
echo "Serving" ${APP_MODULE} "with gunicorn..."
echo "Port:" ${APP_PORT}
echo "Threads:" ${APP_THREADS}

gunicorn -w ${APP_THREADS} -b 0.0.0.0:${APP_PORT} ${APP_MODULE}:app
