from django.conf.urls import url
from dv_apps.datafiles import views

urlpatterns = (

    url(r'^table-preview-json/(?P<datafile_id>\d{1,8})?', views.view_table_preview_json, name='view_table_preview_json'),

)
