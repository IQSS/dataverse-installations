from django.conf.urls import url
from dv_apps.dataverses import views

urlpatterns = (

    url(r'^list/(?P<output_format>\w{1,8})?', views.view_dataverse_list, name='view_dataverse_csv'),

    url(r'^list?', views.view_dataverse_list, name='view_dataverse_list_default'),

)
