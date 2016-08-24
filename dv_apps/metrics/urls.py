from django.conf.urls import url
#from dv_apps.metrics.views import view_dataset_count
from dv_apps.metrics import views_test,\
    views_public_metrics, views_swagger_spec, views_error_test
from dv_apps.metrics.stats_views_datasets import DatasetCountByMonthView,\
    DatasetTotalCounts,\
    DatasetSubjectCounts
from dv_apps.metrics.stats_views_dataverses import DataverseCountByMonthView,\
    DataverseTotalCounts,\
    DataverseAffiliationCounts,\
    DataverseTypeCounts
from dv_apps.metrics.stats_views_files import FileCountByMonthView,\
    FileTotalCountsView,\
    FilesDownloadedByMonthView,\
    FileCountsByContentTypeView,\
    FileExtensionsWithinContentType

from dv_apps.dataverse_auth.decorator import apikey_required

urlpatterns = [

    # views_public_metrics
    url(r'^basic-viz$', views_public_metrics.view_public_visualizations, name='view_public_visualizations'),

    url(r'^basic-viz/last12$', views_public_metrics.view_public_visualizations_last12, name='view_public_visualizations_last12'),

    url(r'^files/types$', views_public_metrics.view_files_by_type, name='view_files_by_type'),

    url(r'^files/extensions$', views_public_metrics.view_file_extensions_within_type, name='view_file_extensions_within_type'),

    # views_test
    url(r'^dv-tree$', views_test.view_dataverse_tree, name='view_dataverse_tree'),

    url(r'^dv-tree.json$', views_test.get_dataverse_tree_json, name='get_dataverse_tree_json'),

    url(r'^dv-tree-full.json$', views_test.get_dataverse_full_tree_json, name='get_dataverse_full_tree_json'),

    url(r'^dv-tree2$', views_test.view_dataverse_tree2, name='view_dataverse_tree2'),


]


urlpatterns += [

    # swagger
    #url(r'^v1/swagger-test.yaml$', views_swagger_spec.view_swagger_spec_test, name='view_swagger_spec_test'),

    url(r'^v1/swagger.yaml$', views_swagger_spec.view_dynamic_swagger_spec, name='view_dynamic_swagger_spec'),

    # API endpoints
    #

    # Dataverses
    url(r'^v1/dataverses/count$', apikey_required(DataverseTotalCounts.as_view()), name='view_dataverse_counts'),

    url(r'^v1/dataverses/count/monthly$', apikey_required(DataverseCountByMonthView.as_view()), name='view_dataverse_counts_by_month'),

    url(r'^v1/dataverses/count/by-affiliation$', apikey_required(DataverseAffiliationCounts.as_view()), name='view_dataverse_counts_by_affiliation'),

    url(r'^v1/dataverses/count/by-type$', apikey_required(DataverseTypeCounts.as_view()), name='view_dataverse_counts_by_type'),



    # Datasets
    url(r'^v1/datasets/count$', apikey_required(DatasetTotalCounts.as_view()), name='view_dataset_counts'),

    url(r'^v1/datasets/count/monthly$', apikey_required(DatasetCountByMonthView.as_view()), name='view_dataset_counts_by_month'),

    url(r'^v1/datasets/count/by-subject$', apikey_required(DatasetSubjectCounts.as_view()), name='view_dataset_counts_by_subject'),

    # Files
    url(r'^v1/files/count$', apikey_required(FileTotalCountsView.as_view()), name='view_files_counts_by_month'),

    url(r'^v1/files/count/monthly$', apikey_required(FileCountByMonthView.as_view()), name='view_files_counts_by_month'),

    url(r'^v1/files/count/by-type$', apikey_required(FileCountsByContentTypeView.as_view()), name='view_files_counts_by_type'),

    url(r'^v1/files/downloads/count/monthly$', apikey_required(FilesDownloadedByMonthView.as_view()), name='view_file_download_counts_by_month'),

    url(r'^v1/files/extensions$', apikey_required(FileExtensionsWithinContentType.as_view()), name='view_file_extensions_within_type'),

]

urlpatterns += [

    url(r'^test-404$', views_error_test.view_test_404, name='view_test_404'),


    url(r'^test-500$', views_error_test.view_test_500, name='view_test_500'),

]
