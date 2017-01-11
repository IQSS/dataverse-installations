from django.conf.urls import url
from dv_apps.dataverses import views

urlpatterns = (
    url(r'^list/?', views.view_dataverse_list, name='view_dataverse_list'),


)
