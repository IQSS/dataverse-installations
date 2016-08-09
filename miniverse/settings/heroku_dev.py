from __future__ import absolute_import
import json
import sys
from os import makedirs
from os.path import join, normpath, isdir, isfile
import dj_database_url

from .base import *

HEROKU_DB_CONFIG = dj_database_url.config()

DATABASES = {
    'django_contrib_db': HEROKU_DB_CONFIG,
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvn_thedata',   #  dvn_thedata dvndb_demo
        'USER': 'postgres', # dv_readonly, postgres
        'PASSWORD': '123',
        'HOST': 'localhost'
    }
}
