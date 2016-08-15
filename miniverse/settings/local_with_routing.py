from __future__ import absolute_import
import json
import sys
from os import makedirs
from os.path import join, normpath, isdir, isfile
from miniverse.testrunners.disable_migrations import DisableMigrations
from .base import *

SECRET_KEY = 'make-a-secret-key'

LOCAL_SETUP_DIR = join(PROJECT_ROOT, 'test_setup')
if not isdir(LOCAL_SETUP_DIR):
    makedirs(LOCAL_SETUP_DIR)

DATABASE_ROUTERS = ['miniverse.settings.db_django_contrib_router.DjangoContribRouter', ]


DATABASES = {

    'miniverse_admin_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LOCAL_SETUP_DIR, 'metrics_auth.db3'),
        'TEST': {
            'MIRROR': 'default',
        },
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb_demo',   #  dvn_thedata dvndb_demo
        'USER': 'postgres', # dv_readonly, postgres
        'PASSWORD': '123',
        'HOST': 'localhost',
    }
}



"""
    'miniverse_admin_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metrics_internal',   #  dvn_thedata dvndb_demo
        'USER': 'rp', # dv_readonly, postgres
        'PASSWORD': '123',
        'HOST': 'localhost',
        'TEST': {
            'MIRROR': 'default',
        },
    },
'miniverse_admin_db': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(LOCAL_SETUP_DIR, 'metrics_auth.db3'),
    'TEST': {
        'MIRROR': 'default',
    },
},

'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dvndb_demo',
    'USER': 'postgres',
    'PASSWORD': '123',
    'HOST': 'localhost'
}

'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dvndb',
    'USER': 'rp',
    'PASSWORD': '123',
    'HOST': 'localhost'
}

'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dvn_thedata',
    'USER': 'postgres',
    'PASSWORD': '123',
    'HOST': 'localhost'
}
"""

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
########## END TOOLBAR CONFIGURATION

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage

    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['USER'] = 'rp'
    DATABASES['default']['PASSWORD'] = '123'

    DATABASES['miniverse_admin_db']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['miniverse_admin_db']['HOST'] = 'localhost'
    DATABASES['miniverse_admin_db']['USER'] = 'rp'
    DATABASES['miniverse_admin_db']['PASSWORD'] = '123'


    # The custom routers we're using to route certain ORM queries
    # to the remote host conflict with our overridden db settings.
    # Set DATABASE_ROUTERS to an empty list to return to the defaults
    # during the test run.

    DATABASE_ROUTERS = []

    MIGRATION_MODULES = DisableMigrations()

    # Set Django's test runner a custom class that will create
    # 'unmanaged' tables
    sys.path.append('/Users/rmp553/Documents/iqss-git/miniverse')
    sys.path.append('/Users/rmp553/Documents/iqss-git/miniverse/miniverse')
    TEST_RUNNER = 'miniverse.testrunners.managed_model_test_runner.ManagedModelTestRunner'
