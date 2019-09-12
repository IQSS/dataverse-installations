# dataverse-installations

## Introduction

This repo is a copy of the "installations" application from https://github.com/IQSS/miniverse that

- powers the map at https://services.dataverse.harvard.edu/miniverse/map/
- provides a dump of all installations at https://services.dataverse.harvard.edu/miniverse/map/installations-json

Some ideas for how to improve this code have already been captured in the "miniverse" issue tracker...

- Make it easier to maintain and make public certain info. about known Dataverse installations: https://github.com/IQSS/miniverse/issues/61
- Make fields in Dataverse installation database mandatory: https://github.com/IQSS/miniverse/issues/63
- Links to installations on dataverse.org map aren't opening in new browser tab: https://github.com/IQSS/miniverse/issues/64

... but more ideas should be contributed in the issue tracker here!

## Requirements

- Python 3.5+

## Quickstart

    python3 -m venv venv

    source venv/bin/activate

    pip install -r requirements.txt

    python manage.py test installations

    rm -rf db.sqlite3

    rm -rf installations/migrations

    python manage.py makemigrations installations

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver

## Bugs

- upload doesn't work from admin

## Think more about

- remove Institutions?
- remove marker from model?
- settings.PROTOCOL
