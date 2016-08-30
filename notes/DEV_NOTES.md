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

## Qtunnel

### Download and unpack tunnel application:

```
curl https://s3.amazonaws.com/quotaguard/qgtunnel-1.0.2.tar.gz | tar xz
```

### You can find url on your QuotaGuard dashboard. This normally is already set on your dyno for the apps that have a QuotaGuard Static addon attached
  - export QUOTAGUARDSTATIC_URL=
  - Heroku dev has url: http://quotaguard6453:b46f0642d9ed@us-east-static-01.quotaguard.com:9293


### Change .qgtunnel configuration file located in main directory.
  - Example for postgres:

```
[qgtunnel.postgres]
accept = "localhost:5432"
connect = "ec2-10-10-10-1.compute-1.amazonaws.com:5432"
```

  - With this configuration tunnel application will listen on your dyno's local port 5432 and all traffic to this local port will go to the remote server (ec2-10-10-10-1.compute-1.amazonaws.com:5432 in this example) via SOCKS5 proxy.

  - For the metrics dev setup:

```
[qgtunnel.postgres]
accept = "localhost:5432"
connect = "demo.dataverse.org:5432"
```

### Change your application configuration to use 127.0.0.1:5432 address instead of db url (ec2-10-10-10-1.compute-1.amazonaws.com:5432 for this configuration example)
  All traffic from the local port will be forwarded to the url in configuration file

```python
# Try some db routing via qtunnel.
# .qgtunnel file has actual host of 'demo.dataverse.org:5432'
DATABASES['default']['HOST'] = '127.0.0.1'
DATABASES['default']['PORT'] = '5432'
```


### Change your Procfile to use tunnel:

  - Example:

```
/bin/qgtunnel gunicorn miniverse.wsgi --log-file - --limit-request-line 8190
```

###  Check heroku log for errors, you can also enable debug mode by doing:

```
export QGTUNNEL_DEBUG=true
```
