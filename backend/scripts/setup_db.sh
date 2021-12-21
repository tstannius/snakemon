#!/bin/bash

set -euo pipefail

# ensure versions dir exists
mkdir -p alembic/versions
# remove any existing database and migrations
rm -f app/snakemon.db; rm -f alembic/versions/*.py

# make migrations
# note the --autogenerate flag, which tells Alembic to use the alembic/env.py target_metadata
alembic revision --autogenerate -m "Init db"

# inspect migration script in alembic/versions and sanity check, before upgrade
alembic upgrade head

# inital data
# note the python module notation
python3 -m app.init_app
