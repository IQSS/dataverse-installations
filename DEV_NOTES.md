(development notes, not instructions)

## Metrics and multiple databases

Working on metrics prototype by pointing Django at an existing dataverse Postgres db.  However, we don't want to add new tables to the Dataverse db:

- Existing db should stay as is--no new tables
- Django contrib apps such as auth, contenttypes, sessions, etc should be in a separate database

Running django contrib apps via migrate:

```
python manage.py migrate contenttypes --database django_contrib_db --run-syncdb
python manage.py createsuperuser --database django_contrib_db
```
