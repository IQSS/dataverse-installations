"""
Settings template for running two databases:
    - Existing Dataverse databases (we only read it)
    - Second database for Django core apps + Miniverse apps

Please read through and change the settings where noted
"""
from __future__ import absolute_import
import sys
from os import makedirs
from os.path import join, isdir
from miniverse.testrunners.disable_migrations import DisableMigrations
from .base import *

# -----------------------------------
# DEBUG
#   - False: Dataverse Key required for API
#       - Includes SQL for many of the API call results
#   - True: Django debug toolbar activated
# -----------------------------------
DEBUG = False   # Should be False in production!

# -----------------------------------
# TIME_ZONE
# -----------------------------------
TIME_ZONE = 'America/New_York'

# -----------------------------------
# secret key
#   Set a new secret key.  hint: https://gist.github.com/mattseymour/9205591
# -----------------------------------
SECRET_KEY = 'my-secret-key'


# -----------------------------------
# ADMINS and MANAGERS
# -----------------------------------

# Receive 500 errors
#
ADMINS = [ ('Raman', 'raman_prasad@harvard.edu'),
    ('Danny Brooke', 'dannybrooke@g.harvard.edu')]

# Receive 404 errors
#
MANAGERS = ADMINS


# -----------------------------------
# CACHE settings for visualzations and API
# -----------------------------------
METRICS_CACHE_VIEW = True
METRICS_CACHE_VIEW_TIME = 60 * 60 * 2   # Cache for visualizations
METRICS_CACHE_API_TIME = 60 * 15    # Cache for API endpoints

# -----------------------------------
# Swagger Specs.  The following attributes must be set to properly
# generate the swagger spec and use the swagger UI
# -----------------------------------
SWAGGER_HOST = 'services.dataverse.harvard.edu' # temp, this should come from sites framework
SWAGGER_SCHEME = 'https'

# -----------------------------------
# Database routing.
#   e.g. between the Dataverse db and Django db
# -----------------------------------
DATABASE_ROUTERS = ['miniverse.db_routers.db_dataverse_router.DataverseRouter',]

# -----------------------------------
# URL of the Dataverse db being read
# -----------------------------------
DATAVERSE_INSTALLATION_URL = 'https://dataverse.harvard.edu'

# -----------------------------------
# Database Setup
#   - default -> Create a new db for the django/miniverse specific apps
#       - May be any relational db type: postgres, sqlite, etc
#   - dataverse -> Read-only users for the Dataverse Posgres db
# -----------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'miniverse_default',
        'USER': 'miniverse_user',     # Can create/edit tables
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'dataverse': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dvndb',
        'USER': 'miniverse_dv_user',     # Set to a read-only user
        'PASSWORD': 'the-password',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'MIRROR': 'default', # For running tests, only create 1 db
        },
    }
}


# -----------------------------------
# A list of strings representing the
# host/domain names that this Django site can serve
#  See: https://docs.djangoproject.com/en/1.9/ref/settings/#allowed-hosts
# -----------------------------------
ALLOWED_HOSTS = ('services.datavarse.harvard.edu',\
        'static-ip-of-server')

# -----------------------------------
# Need to set when RestrictAdminMiddleware is active
# -----------------------------------
INTERNAL_IPS = ('127.0.0.1',)


# -----------------------------------
# Optional MIDDLEWARE_CLASSES
# -----------------------------------
MIDDLEWARE_CLASSES += [
    # Restrict by IP address
    #'dv_apps.admin_restrict.middleware.RestrictAdminMiddleware',
    # Email about broken 404s
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

# -----------------------------------
# Mail settings
# see: https://docs.djangoproject.com/en/1.10/ref/settings/#email-host
# -----------------------------------
EMAIL_HOST = 'ackroyd.harvard.edu'
EMAIL_PORT = 587
#EMAIL_HOST_USER = 'fill in'
#EMAIL_HOST_PASSWORD = 'fill in'
DEFAULT_FROM_EMAIL = 'raman_prasad@harvard.edu'
EMAIL_USE_TLS = True


# -----------------------------------
# root urls file
# -----------------------------------
ROOT_URLCONF = 'miniverse.urls_lts_prod'

# -----------------------------------
# cookie name
# -----------------------------------
SESSION_COOKIE_NAME = 'dv_metrics_lts'

# -----------------------------------
# Where static files are collected
# -----------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
#

# "The absolute path to the directory where collectstatic will collect static files for deployment."
STATIC_ROOT = '"/var/www/services.dataverse.harvard.edu/static/"'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# e.g. Django gathers these files and copies them to the STATICROOT above
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

# -----------------------------------
# Where media files are located
#   These are user uploaded files.
#   - In this case, logos uploaded by an administrator
# -----------------------------------
# "Absolute filesystem path to the directory that will hold user-uploaded files.""
# This MUST differ from STATIC_ROOT
MEDIA_ROOT = "/var/www/services.dataverse.harvard.edu/media/"
MEDIA_URL = "/media/"   # This MUST differ from STATIC_URL


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

    # These credentials should be able to create a database named: 'test_miniverse_default'
    #
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['USER'] = 'miniverse_user'
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
