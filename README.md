# miniverse
Reference/Debug use: Using the Django ORM to explore the Dataverse database

Documentation

https://docs.google.com/document/d/1ThlSbw9LWtd12UzUmPxhXdlIlyCiROtBXdcIm8OGc2k/edit?usp=sharing


# Setting Notes (read)

## Restricted Django Admin - ```RestrictAdminMiddleware```

By default Django Admin access is restricted to addresses listed in ```settings.INTERNAL_IPS```.

Admin users who are not coming from an IP listed in ```settings.INTERNAL_IPS``` will receive a 404 error.

- To completely disable this restriction:
    - In setttings.MIDDLEWARE_CLASSES, remove: ```dv_apps.admin_restrict.middleware.RestrictAdminMiddleware```
- To add acceptable addresses to ```settings.INTERNAL_IPS```
    - You can add full addresses.  e.g. 140.247.10.10
        - e.g., ```INTERNAL_IPS = ('140.247.10.10',)```
    - You can add the 1st two segments of the address:
        - e.g., ```INTERNAL_IPS = ('140.247', ..)```
    - You can add the 1st three segments of the address:
        - e.g., ```INTERNAL_IPS = ('140.247.10', ...)```
    - For running django's test server, the default is:
        - e.g., ```INTERNAL_IPS = ('127.0.0.1', ...)```

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
