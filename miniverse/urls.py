from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from dv_apps.metrics import views_public_metrics
admin.site.site_header = 'Dataverse DB'

URL_PREFIX = 'miniverse/'


urlpatterns = [
    # Examples:
    # url(r'^$', 'miniverse.views.home', name='home'),
    url(r'^%sdr2m/' % URL_PREFIX, include('dv_apps.dvobjects.urls')),

    url(r'^%sdataset/' % URL_PREFIX, include('dv_apps.datasets.urls')),

    url(r'^%smap/' % URL_PREFIX, include('dv_apps.installations.urls')),

    url(r'^%smetrics/' % URL_PREFIX, include('dv_apps.metrics.urls')),

    url(r'^%sdvobjects/' % URL_PREFIX, include('dv_apps.dvobject_api.urls')),

    url(r'^%sminiverse-admin/' % URL_PREFIX, include(admin.site.urls)),

    url(r'^%sminiverse-admin/' % URL_PREFIX, include(admin.site.urls)),

    url(r'^/?$', views_public_metrics.view_homepage_placeholder, name='view_homepage_placeholder'),


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
