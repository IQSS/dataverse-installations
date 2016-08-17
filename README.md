# miniverse
Reference/Debug use: Using the Django ORM to explore the Dataverse database

Documentation

https://docs.google.com/document/d/1ThlSbw9LWtd12UzUmPxhXdlIlyCiROtBXdcIm8OGc2k/edit?usp=sharing


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
