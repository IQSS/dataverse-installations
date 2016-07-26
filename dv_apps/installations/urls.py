from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.Map, name='Map'),

    #url(r'^dataverse/(?P<institution_name>\S*)/$', views.installations, name='newinstitution'),
    #url(r'^$', views.index, name='installations_index'),
    #url(r'^$', views.institutions, name='institution_index'),
]
