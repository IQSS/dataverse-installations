"""
Hanlde Slack channel requests
"""
from django.conf.urls import url
from dv_apps.quality_checks import views

urlpatterns = (

    url(r'^filesize-zero$', views.view_filesize_zero, name='view_filesize_zero'),

)
