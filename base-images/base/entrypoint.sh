#!/bin/bash
set -x
python3 ./config.py "$CONF_DIR"
exec "$@"