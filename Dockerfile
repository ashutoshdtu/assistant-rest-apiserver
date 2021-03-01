FROM python:alpine3.12
#FROM python:2.7.15-alpine3.8 

LABEL maintainer="Ashutosh Mishra <ashutoshdtu@gmail.com>"

ENV APP_PORT 8000
ENV PORT ${APP_PORT}

# Expose ports
EXPOSE ${APP_PORT}

# Add source code
WORKDIR /
COPY . .
WORKDIR /app

# Make scripts executable
RUN chmod +x /start.sh /entrypoint.sh /app/install.sh /app/prestart.sh /app/serve.sh
# RUN apk add git
RUN /app/install.sh

# Add Tini init system
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "-g", "--", "/entrypoint.sh"]

# Pass your environment variables

ENV APP_HOST_NAME 0.0.0.0
ENV APP_MODULE rest_apiserver
ENV APP_THREADS 2

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]
