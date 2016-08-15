from __future__ import absolute_import
import os
from os.path import join#, normpath, isdir, isfile
import dj_database_url

from .base import *

# Set the secret key
print 'pre secret key'
SECRET_KEY = os.environ['SECRET_KEY']

# Cookie name
SESSION_COOKIE_NAME = 'dv_metrics_dev'


#INTERNAL_IPS = ()   # Heroku IP

ALLOWED_HOSTS = ['54.235.72.96',]


## Database settings via Heroku url
HEROKU_DB_CONFIG = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(HEROKU_DB_CONFIG)

# Heroku specific urls
ROOT_URLCONF = 'miniverse.urls_heroku_dev'


"""
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
"""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
