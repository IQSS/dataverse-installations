from django.conf.urls import url

from dv_apps.dvobject_api import views_dataverses
#, views_api, views_test,\
#    views_public_metrics, views_swagger
#from dv_apps.metrics.stats_views_datasets import DatasetCountByMonthView,\
#    DatasetTotalCounts

urlpatterns = [

    # Dataverses
    url(r'^api/v1/dataverses/(?P<dataverse_id>\d{1,8})$', views_dataverses.view_single_dataverse, name='view_single_dataverse'),

    # Datasets

    # Files

]
