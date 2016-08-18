# miniverse
Reference/Debug use: Using the Django ORM to explore the Dataverse database

Documentation

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
