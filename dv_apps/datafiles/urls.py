from django.conf.urls import url
from dv_apps.datafiles import views, views_downloads

urlpatterns = (

    url(r'^table-preview-json/(?P<datafile_id>\d{1,8})?',
        views.view_table_preview_json,
        name='view_table_preview_json'),

    url(r'^table-preview-html/(?P<datafile_id>\d{1,8})?',
        views.view_table_preview_html,
        name='view_table_preview_html'),

    url(r'^download-bytes/(?P<selected_year>(19|20)\d{2})$',
        views_downloads.view_monthly_downloads,
        name='view_monthly_downloads_by_year'),

    url(r'^download-bytes/$',
        views_downloads.view_monthly_downloads,
        name='view_monthly_downloads'),

)
