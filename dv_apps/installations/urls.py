from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.view_map, name='view_map'),

    url(r'^dataverse-org$', views.view_map_dataverse_org, name='view_map_dataverse_org'),

]
