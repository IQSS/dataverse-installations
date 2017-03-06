"""
Hanlde Slack channel requests
"""
from django.conf.urls import url
from dv_apps.quality_checks import views

urlpatterns = (

    url(r'^dashboard$',
        views.view_qc_dashboard,
        name='view_qc_dashboard'),

    url(r'^filesize-zero-local-list$',
        views.view_filesize_zero_local_list,
        name='view_filesize_zero_local_list'),

    url(r'^no-checksum-local-list$',
        views.view_no_checksum_list,
        name='view_no_checksum_list_local'),

    url(r'^no-checksum-harvested-list$',
        views.view_no_checksum_list_harvested,
        name='view_no_checksum_list_harvested'),

)
