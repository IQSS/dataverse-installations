from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #url(r'^installations-json$', views.view_installations_json, name='view_installations_json'),
    #path(r'^installations-json$', views.view_installations_json, name='view_installations_json'),
    path('installations.json', views.view_installations_json, name='view_installations_json'),
]
