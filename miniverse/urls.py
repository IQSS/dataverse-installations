from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

admin.site.site_header = 'Dataverse DB'

urlpatterns = [
    # Examples:
    # url(r'^$', 'miniverse.views.home', name='home'),
    url(r'^dr2m/', include('dv_apps.dvobjects.urls')),

    url(r'^dataset/', include('dv_apps.datasets.urls')),

    url(r'^metrics/', include('dv_apps.metrics.urls')),

    url(r'^miniverse-admin/', include(admin.site.urls)),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
