from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Dataverse DB'

urlpatterns = [
    # Examples:
    # url(r'^$', 'miniverse.views.home', name='home'),
    url(r'^miniverse/dr2m/', include('dv_apps.dvobjects.urls')),

    url(r'^miniverse/dataset/', include('dv_apps.datasets.urls')),

    url(r'^miniverse/map/', include('dv_apps.installations.urls')),

    url(r'^miniverse/metrics/', include('dv_apps.metrics.urls')),

    url(r'^miniverse/dvobjects/', include('dv_apps.dvobject_api.urls')),

    url(r'^miniverse/miniverse-admin/', include(admin.site.urls)),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^debug/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += patterns('',
    #    url(r'^__debug__/', include(debug_toolbar.urls)),
    #)
