### __DOCS IN PROGRESS..MORE COMPLETE BY AUG. 26__

# Miniverse

This repository may be configured to directly read an existing Dataverse 4.x database.
This read access includes the ability to pull metrics from a Dataverse installation.  

However, the repository was initially created as a way to explore/debug/prototype.

## Functions

- In use:
  - Retrieve basic metrics via API or as visualizations
  - Map visualization of Dataverse affiliations
  - Contributions by [@jcabanas17](https://github.com/jcabanas17), [@emunn](https://github.com/emunn),
- Explore/Prototype
  - Using the Django ORM to explore the Dataverse database, create queries that are later translated to Java code
  - Store cached metadata in JSON documents.   


## Metrics set-up


### Set-up

This describes a set-up with two databases:
  1. An existing Dataverse db in Postgres and credentials to at least read the db tables
    - This Database is unmanaged.  e.g. Django does not update or attempt to update the tables.
    - With proper user credentials, you can edit records via the Django Admin--but **DON'T** do this against a production Dataverse
  2. A database for Django to create tables needed for the map and administration.  
    - This can be any relational db.  (Have used Postgres and sqlite)


### Step 1: Pip install, y'all

This assumes you have [pip](https://pip.pypa.io/en/stable/installing/) and [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) already running.

- Pull down the miniverse repository
- Install the requirements:

```
# cd into the repo
cd miniverse

# install the basic requirements
pip install -r requirements/local.txt
```

### Step 2: Make a settings file

Create a settings file for a two database set-up.

```
# Make your own settings file: copy "miniverse/settings/local_with_routing.py"
#
cp miniverse/settings/local_with_routing.py miniverse/settings/local_settings.py

```



### Maps Documentation

https://docs.google.com/document/d/1ThlSbw9LWtd12UzUmPxhXdlIlyCiROtBXdcIm8OGc2k/edit?usp=sharing


# Setting Notes (read)

## Restricted Django Admin - ```RestrictAdminMiddleware```

Using middleware, the Django Admin access may be restricted to addresses listed in ```settings.INTERNAL_IPS```.

When this middeware is active, users going to Django admin urls who are not coming from an IP listed in ```settings.INTERNAL_IPS``` will receive a 404 error.

- To enable this restriction:
    - In settings.MIDDLEWARE_CLASSES, add: ```dv_apps.admin_restrict.middleware.RestrictAdminMiddleware```
    - Example for ```settings.local``` which is importing from ```settings.base```:

```python
MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
]
```

- To add acceptable addresses to ```settings.INTERNAL_IPS```
    - You can add full addresses.  e.g. 211.247.10.10
        - e.g., ```INTERNAL_IPS = ('211.247.10.10',)```
    - You can add the 1st two segments of the address:
        - e.g., ```INTERNAL_IPS = ('140.247', '211.247.10.10',)```
    - You can add the 1st three segments of the address:
        - e.g., ```INTERNAL_IPS = ('140.247.10', '211.247.10.10',)```
    - For running django's test server, the default is:
        - e.g., ```INTERNAL_IPS = ('127.0.0.1',)```

  - Dev note: The code for ```RestrictAdminMiddleware``` is in ```dv_apps/middeware.py```
---


# Load Heroku markers

## Preload to S3.  

- Can use boto script in:

```
scripts/copy_logos_to_s3.py
```

- Add creds to script and run

## Load fixtures

```heroku run python manage.py loaddata dv_apps/installations/fixtures/heroku_installations_2016_0811.json
```
