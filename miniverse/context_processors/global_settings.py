"""
reference: https://chriskief.com/2013/09/19/access-django-constants-from-settings-py-in-a-template/
"""
from django.conf import settings

def settings_for_templates(request):
    return {
        'DEBUG': settings.DEBUG,
        #'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
