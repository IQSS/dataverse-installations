from django.conf.urls import url

from dv_apps.dvobject_api import views_dataverses, views_datasets


urlpatterns = [

    # Dataverses
    url(r'^api/v1/dataverses/by-id/(?P<dataverse_id>\d{1,8})$', views_dataverses.view_single_dataverse_by_id, name='view_single_dataverse_by_id'),

    url(r'^api/v1/dataverses/(?P<alias>\w{1,30})$', views_dataverses.view_single_dataverse_by_alias, name='view_single_dataverse_by_alias'),

    # Datasets
    url(r'^api/v1/datasets/by-id/(?P<dataset_version_id>\d{1,8})$', views_datasets.view_single_dataset_by_id, name='view_single_dataset_by_id'),


]
