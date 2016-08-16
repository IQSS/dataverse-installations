(development notes, not instructions)

- [ ] Tests
- [ ] Multiple dbs on heroku
- [ ] S3 on heroku for uploads
- 


## Metrics and multiple databases

Working on metrics prototype by pointing Django at an existing dataverse Postgres db.  However, we don't want to add new tables to the Dataverse db:

- Existing db should stay as is--no new tables
- Django contrib apps such as auth, contenttypes, sessions, etc should be in a separate database

Running django contrib apps via migrate:

```
python manage.py migrate contenttypes --database miniverse_admin_db --run-syncdb
python manage.py createsuperuser --database miniverse_admin_db
```

##

- users per month
- how many files have statistics
    - needs datatable list

## Install (need to detail in readme)

- pip install
- test db download and import
    - postgres user: postgres|123
    - postgres db: dvndb_demo
    - psql dvndb_demo < file-with-dv-sql-dump.sql
- configure settings
- postactivate
    export DJANGO_DEBUG=True
    export DJANGO_SETTINGS_MODULE=miniverse.settings.local
- (does readonly user work?)
- python manage.py migrate
- python manage.py createsuperuser
- python manage check
- python manage.py loaddata dv_apps/installations/fixtures/installations.json
- python manage.py runserver

## readonly user

GRANT SELECT ON ALL TABLES IN SCHEMA public TO dv_readonly;

## tree view 2

http://bl.ocks.org/robschmuecker/7926762


## swagger ui

127.0.0.1:8000/static/swagger-ui/index.html
