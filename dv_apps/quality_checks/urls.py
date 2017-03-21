"""
Hanlde Slack channel requests
"""
from django.conf.urls import url
from dv_apps.quality_checks import views, views_notifications

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

    url(r'^bad-ingest-list$',
        views.view_bad_ingest_list,
        name='view_bad_ingest_list'),

    url(r'^in-progress-ingest-list$',
        views.view_in_progress_ingest_list,
        name='view_in_progress_ingest_list'),

    url(r'^broken-notifications$',
        views_notifications.view_broken_notifications,
        name='view_broken_notifications'),

    url(r'^broken-notifications/details/(?P<model_name>\w{4,40})$',
        views_notifications.view_broken_notification_details,
        name='view_broken_notification_details'),

)
