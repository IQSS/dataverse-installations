from django.conf.urls import url
#from dv_apps.metrics.views import view_dataset_count
from dv_apps.metrics import views, views_api, views_test,\
    views_public_metrics, views_swagger
from dv_apps.metrics.stats_views_datasets import DatasetCountByMonthView
from dv_apps.metrics.stats_views_dataverses import DataverseCountByMonthView,\
    DataverseTotalCounts,\
    DataverseAffiliationCounts,\
    DataverseTypeCounts
from dv_apps.metrics.stats_views_files import FileCountByMonthView,\
    FileTotalCountsView

urlpatterns = [

    # views_public_metrics
    url(r'^basic-viz$', views_public_metrics.view_public_visualizations, name='view_public_visualizations'),

    url(r'^basic-viz/last12$', views_public_metrics.view_public_visualizations_last12, name='view_public_visualizations_last12'),

    url(r'^files/types$', views_public_metrics.view_files_by_type, name='view_files_by_type'),

    url(r'^files/extensions$', views_public_metrics.view_file_extensions_within_type, name='view_file_extensions_within_type'),

    # views_test
    url(r'^dv-tree$', views_test.view_dataverse_tree, name='view_dataverse_tree'),

    url(r'^dvtree.json$', views_test.get_dataverse_tree_json, name='get_dataverse_tree_json'),

    url(r'^dv-tree2$', views_test.view_dataverse_tree2, name='view_dataverse_tree2'),


    url(r'^datasets/count/simple2$', views.view_simple_dataset_count2, name='view_simple_dataset_count2'),
]


urlpatterns += [

    # swagger
    url(r'^v1/swagger-test.yaml$', views_swagger.view_swagger_spec_test, name='view_swagger_spec_test'),

    url(r'^v1/swagger.yaml$', views_swagger.view_dynamic_swagger_spec, name='view_dynamic_swagger_spec'),

    # API endpoints
    #

    # Dataverses
    url(r'^v1/dataverses/count$', DataverseTotalCounts.as_view(), name='view_dataverse_counts'),

    url(r'^v1/dataverses/count/monthly$', DataverseCountByMonthView.as_view(), name='view_dataverse_counts_by_month'),

    url(r'^v1/dataverses/count/by-affiliation$', DataverseAffiliationCounts.as_view(), name='view_dataverse_counts_by_affiliation'),

    url(r'^v1/dataverses/count/by-type$', DataverseTypeCounts.as_view(), name='view_dataverse_counts_by_type'),



    # Datasets
    url(r'^v1/datasets/count/monthly$', DatasetCountByMonthView.as_view(), name='view_dataset_counts_by_month'),

    # Files
    url(r'^v1/files/count$', FileTotalCountsView.as_view(), name='view_files_counts_by_month'),

    url(r'^v1/files/count/monthly$', FileCountByMonthView.as_view(), name='view_files_counts_by_month'),


]
