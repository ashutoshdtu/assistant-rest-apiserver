#!/bin/sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    sh $PRE_START_PATH
else 
    echo "There is no script $PRE_START_PATH"
fi

echo "Port: $PORT"

SERVER_PATH=/app/serve.sh
# Start Supervisor, with Nginx and uWSGI
# exec /usr/bin/supervisord
exec ${SERVER_PATH}