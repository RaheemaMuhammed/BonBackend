#!/bin/sh

set -o errexit
set -o nounset


# Run a Celery worker
celery -A backend worker --loglevel=info
