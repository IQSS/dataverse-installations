from __future__ import absolute_import
import json
import sys
from os import makedirs
from os.path import join, normpath, isdir, isfile
from miniverse.testrunners.disable_migrations import DisableMigrations
from .base import *

SECRET_KEY = 'DEV-j94xnz*dj5f@_6-gt@ov)yjbcx0uagb7sv9a0j-(jo)j%m$el%'

METRICS_CACHE_VIEW = True
METRICS_CACHE_VIEW_TIME = 60 * 60 * 2   # 2 HOURS
METRICS_CACHE_API_TIME = 30 * 60 

LOCAL_SETUP_DIR = join(PROJECT_ROOT, 'test_setup')
if not isdir(LOCAL_SETUP_DIR):
    makedirs(LOCAL_SETUP_DIR)

DATABASE_ROUTERS = ['miniverse.db_routers.db_dataverse_router.DataverseRouter',]

DEBUG = True

# Need when running DEBUG = False
ALLOWED_HOSTS = ('127.0.0.1', )

# Need to set when RestrictAdminMiddleware is active
INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LOCAL_SETUP_DIR, 'miniverse_auth.db3'),
    },
    'dataverse': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb_demo',   #  dvn_thedata dvndb_demo, dvndb
        'USER': 'postgres', # dv_readonly, postgres
        'PASSWORD': '123',
        'HOST': 'localhost',
        'TEST': {
            'MIRROR': 'default',
        },
    }
}

"""
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metrics_internal',   #  dvn_thedata dvndb_demo
        'USER': 'rp', # dv_readonly, postgres
        'PASSWORD': '123',
        'HOST': 'localhost',
        },
    },
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

########## END TOOLBAR CONFIGURATION

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage

    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['USER'] = 'rp'
    DATABASES['default']['PASSWORD'] = '123'

    # For the testing, only one database is created, using MIRROR:
    #  - See: https://docs.djangoproject.com/en/1.10/topics/testing/advanced/#testing-primary-replica-configurations
    #DATABASES['dataverse']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    #DATABASES['dataverse']['HOST'] = 'localhost'
    #DATABASES['dataverse']['USER'] = 'rp'
    #DATABASES['dataverse']['PASSWORD'] = '123'


    # The custom routers we're using to route certain ORM queries
    # to the remote host conflict with our overridden db settings.
    # Set DATABASE_ROUTERS to an empty list to return to the defaults
    # during the test run.
    DATABASE_ROUTERS = []

    MIGRATION_MODULES = DisableMigrations()

    # Set Django's test runner a custom class that will create
    # 'unmanaged' tables
    TEST_RUNNER = 'miniverse.testrunners.managed_model_test_runner.ManagedModelTestRunner'

    # Disable timezone awareness to False to avoid warnings when loading fixtures
    #   e.g. to avoid:  RuntimeWarning: (some object)received a naive datetime (2016-08-16
    #        09:25:41.349000) while time zone support is active.
    USE_TZ = False
