"""
WSGI config for LTS deployment using miniverse virtualenv.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniverse.settings.lts_settings")

activate_env=os.path.expanduser("~/.virtualenvs/miniverse/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

application = get_wsgi_application()
