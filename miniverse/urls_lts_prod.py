"""
LTS (Library Technical Systems) Production URLs
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Dataverse Metrics (Miniverse)'

URL_PREFIX = ''


urlpatterns = [
    # Examples:
    # url(r'^$', 'miniverse.views.home', name='home'),
    url(r'^%sdr2m/' % URL_PREFIX, include('dv_apps.dvobjects.urls')),

    url(r'^%sdataset/' % URL_PREFIX, include('dv_apps.datasets.urls')),

    url(r'^%smap/' % URL_PREFIX, include('dv_apps.installations.urls')),

    url(r'^%smetrics/' % URL_PREFIX, include('dv_apps.metrics.urls')),

    url(r'^%sdvobjects/' % URL_PREFIX, include('dv_apps.dvobject_api.urls')),

    url(r'^%sminiverse-admin/' % URL_PREFIX, include(admin.site.urls)),

]
