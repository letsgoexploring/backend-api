#!/bin/bash -ex

exec gunicorn api.app:app -b 0.0.0.0:${PORT:-5000} \
                      -w ${WEB_CONCURRENCY:-1} \
                      --error-logfile - \
                      --access-logfile - \
                      --log-level ${LOGLEVEL:-info}
