"""
Settings template for running two databases:
    - Existing Dataverse databases (we only read it)
    - Second database for Django core apps + Miniverse apps

Please read through and change the settings where noted
"""
from __future__ import absolute_import
import sys
from os import makedirs, environ
from os.path import join, isdir
from miniverse.testrunners.disable_migrations import DisableMigrations
from miniverse.settings.base import *

# -----------------------------------
# DEBUG
#   - True: Dataverse Key required for API
#       - Includes SQL for many of the API call results
# -----------------------------------
DEBUG = True   #True False

# -----------------------------------
# TIME_ZONE
# -----------------------------------
TIME_ZONE = 'America/New_York'

# -----------------------------------
# Secret key
# -----------------------------------
SECRET_KEY = 'DEV-j94xnz*dj5f@_6-gt@ov)yjbcx0uagb7sv9a0j-(jo)j%m$el%'

# -----------------------------------
# Metrics cache settings
# -----------------------------------
METRICS_CACHE_VIEW = False
METRICS_CACHE_VIEW_TIME = 60 * 60 * 2   # Cache for visualizations
METRICS_CACHE_API_TIME = 60 * 15    # Cache for API endpoints

# -----------------------------------
# For local runs, this directory will include:
#   - static files (after running 'collectstatic')
#   - optional, sqlite db if that's used for the Django apps db
# -----------------------------------
LOCAL_SETUP_DIR = join(PROJECT_ROOT, 'test_setup')
if not isdir(LOCAL_SETUP_DIR):
    makedirs(LOCAL_SETUP_DIR)

# -----------------------------------
# Database routing.
#   e.g. between the Dataverse db and Django db
# -----------------------------------
DATABASE_ROUTERS = ['miniverse.db_routers.db_dataverse_router.DataverseRouter',]

# -----------------------------------
# URL of the Dataverse db being read
# -----------------------------------
#DATAVERSE_INSTALLATION_URL = 'https://demo.dataverse.org'
DATAVERSE_INSTALLATION_URL = 'https://dataverse.harvard.edu'

# -----------------------------------
# Database Setup
#   - default -> Create a new db for the django/miniverse specific apps
#       - May be any relational db type: postgres, sqlite, etc
#   - dataverse -> Read-only users for the Dataverse Posgres db
# -----------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LOCAL_SETUP_DIR, 'miniverse_default.db3'),
    },
    'dataverse': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb',  # dvndb_demo, dvn_thedata, dvndb
        'USER': 'postgres',     # Set to a read-only user
        'PASSWORD': '123',
        'HOST': 'localhost',
        'TEST': {
            'MIRROR': 'default', # For running tests, only create 1 db
        },
    }
}


# -----------------------------------
# Need when running DEBUG = False
# -----------------------------------
ALLOWED_HOSTS = ('127.0.0.1', 'dd7be506.ngrok.io')

# -----------------------------------
# Need to set when RestrictAdminMiddleware is active
# -----------------------------------
INTERNAL_IPS = ('127.0.0.1',)


# -----------------------------------
# Slackbot
# -----------------------------------
SLACK_USERNAME = 'dvbot'
SLACK_BOT_TOKEN = environ.get('SLACK_BOT_TOKEN')
BOT_ID =  environ.get('BOT_ID')
SLACK_WEBHOOK_SECRET = environ.get('SLACK_WEBHOOK_SECRET')

# -----------------------------------
# Optional MIDDLEWARE_CLASSES
# -----------------------------------
MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    #'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
    # Email about broken 404s
    #'django.middleware.common.BrokenLinkEmailsMiddleware',
]

# -----------------------------------
# cookie name
# -----------------------------------
SESSION_COOKIE_NAME = 'dv_metrics'

# -----------------------------------
# Where static files are collected
# -----------------------------------
STATIC_ROOT = join(LOCAL_SETUP_DIR, 'staticfiles')
if not isdir(STATIC_ROOT):
    makedirs(STATIC_ROOT)


# -----------------------------------
# Django Debug TOOLBAR CONFIGURATION
# -----------------------------------
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
# -----------------------------------
INSTALLED_APPS += (
    'debug_toolbar',
    'django.contrib.admindocs',
)

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html

# -----------------------------------
# For running tests:
#   - Only create 1 test database it has to be a Postgres db
#   - Remove the Database routing
#   - Disable migrations.  e.g., We don't want to run them
#   - Set a new TEST_RUNNER:
#          - We want to *create* unmanaged tables in the test db
#   - Disable timezone awareness for fixture loading
# -----------------------------------
if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage

    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['USER'] = 'rp'
    DATABASES['default']['PASSWORD'] = '123'

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
