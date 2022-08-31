#!/usr/bin/env sh
set -eu
envsubst '\${BACKEND_HOST}\' < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.template.conf
exec "$@"