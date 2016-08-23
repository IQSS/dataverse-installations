from __future__ import absolute_import
import json
import sys
from os import makedirs
from os.path import join, normpath, isdir, isfile

from .base import *

SECRET_KEY = 'make-a-secret-key'

LOCAL_SETUP_DIR = join(PROJECT_ROOT, 'test_setup')
if not isdir(LOCAL_SETUP_DIR):
    makedirs(LOCAL_SETUP_DIR)

#DATABASE_ROUTERS = ['miniverse.settings.db_router_auth.AuthRouter', 'miniverse.settings.db_router_dataverse.DataverseRouter']

DATABASES = {
    'auth_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LOCAL_SETUP_DIR, 'metrics_auth.db3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb_demo',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost'
    },
    'xdataverse': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb_demo',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost'
    }

}

SESSION_COOKIE_NAME = 'dv_metrics'

# where static files are collected
STATIC_ROOT = join(LOCAL_SETUP_DIR, 'staticfiles')
if not isdir(STATIC_ROOT):
    makedirs(STATIC_ROOT)


########## TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
    'django.contrib.admindocs',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
]

########## END TOOLBAR CONFIGURATION


MEDIA_ROOT = join(PROJECT_ROOT,"media")

MEDIA_URL = '/media/'
