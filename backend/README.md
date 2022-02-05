# Setup
### Setup database
##### Setup Alembic
```
# create alembic.ini and alembic/
cd snakemon
alembic init alembic

# modify alembic.ini and alembic/env.py c.f. fastapi template
# check correct db url used
# check correct target_metadata
# check correct run_migrations_online / run_migrations_offline context / connectable params

# commit and make migrations
# TODO: check if --autogenerate needed
alembic revision -m "My message"

# inspect migration script in alembic/versions and sanity check, before upgrade
alembic upgrade head

# later ... 
alembic revision -m "Add a column"
alembic upgrade head
```

##### Initialize database
```
# ensure versions dir exists
mkdir -p alembic/versions
# remove any existing database and migrations
rm -f app/snakemon.db; rm -f alembic/versions/*.py

# make migrations
# note the --autogenerate flag, which tells Alembic to use the alembic/env.py target_metadata
alembic revision --autogenerate -m "Init db"

# inspect migration script in alembic/versions and sanity check, before upgrade
alembic upgrade head

# run script to initalize db with user and data
# note that the script must be run as a library module for imports to work
python3 -m app.init_app
```

### Run backend
```
cd backend
uvicorn app.main:app --reload
```