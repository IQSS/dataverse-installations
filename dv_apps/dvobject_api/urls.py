from django.conf.urls import url

from dv_apps.dvobject_api import views_dataverses,\
        views_datasets,\
        views_composable


urlpatterns = [

    # Dataverses
    url(r'^api/v1/dataverses/by-id/(?P<dataverse_id>\d{1,8})$', views_dataverses.view_single_dataverse_by_id, name='view_single_dataverse_by_id'),

    url(r'^api/v1/dataverse/by-alias/(?P<alias>\w{1,30})$', views_dataverses.view_single_dataverse_by_alias, name='view_single_dataverse_by_alias'),

    # Datasets
    url(r'^api/v1/datasets/by-id/(?P<dataset_id>\d{1,8})$', views_datasets.view_single_dataset, name='view_single_dataset'),

    url(r'^api/v1/datasets/by-persistent-id$', views_datasets.view_dataset_by_persistent_id, name='view_dataset_by_persistent_id'),

    url(r'^api/v1/datasets/by-version-id/(?P<dataset_version_id>\d{1,8})$', views_datasets.view_dataset_by_version, name='view_dataset_by_version'),

    # -----------------------------
    # Composable dataset
    # -----------------------------
    # by id
    url(r'^api/v1/datasets/composable/by-id/(?P<dataset_id>\d{1,8})$', views_composable.view_side_by_side1, name='view_side_by_side1'),

    # by persidentId
    url(r'^api/v1/datasets/composable/by-persistent-id$', views_composable.view_side_by_side1_by_persistent_id, name='view_side_by_side1_by_persistent_id'),




    # Files
    #url(r'^api/v1/datasets/by-id/(?P<dataset_version_id>\d{1,8})$', #views_datasets.view_dataset_by_version_id, name='view_dataset_by_version_id'),

]
