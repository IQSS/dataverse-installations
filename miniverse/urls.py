from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Dataverse DB'

urlpatterns = [
    # Examples:
    # url(r'^$', 'miniverse.views.home', name='home'),
    url(r'^dr2m/', include('dv_apps.dvobjects.urls')),

    url(r'^dataset/', include('dv_apps.datasets.urls')),

    url(r'^map/', include('dv_apps.installations.urls')),

    url(r'^metrics/', include('dv_apps.metrics.urls')),

    url(r'^miniverse-admin/', include(admin.site.urls)),


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
