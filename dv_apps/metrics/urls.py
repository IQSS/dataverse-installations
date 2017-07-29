from django.conf.urls import url

from dv_apps.metrics import views_test,\
    views_public_metrics, views_swagger_spec, views_error_test,\
    views_maintenance
# Dataset metrics
from dv_apps.metrics.stats_views_datasets import DatasetCountByMonthView,\
    DatasetTotalCounts,\
    DatasetSubjectCounts

from dv_apps.metrics.stats_views_dataset_bins import FilesPerDatasetStats,\
    BytesPerDatasetStats

# Dataverse metrics
from dv_apps.metrics.stats_views_dataverses import DataverseCountByMonthView,\
    DataverseTotalCounts,\
    DataverseAffiliationCounts,\
    DataverseTypeCounts

# File metrics
from dv_apps.metrics.stats_views_files import FileCountByMonthView,\
    FileTotalCountsView,\
    FilesDownloadedByMonthView,\
    FileCountsByContentTypeView,\
    FileExtensionsWithinContentType

from dv_apps.dvobject_api.api_view_dataverses import DataverseByIdView,\
    DataverseByAliasView

from dv_apps.dvobject_api.api_view_datasets import DatasetByIdView,\
    DatasetByPersistentIdView

urlpatterns = [

    # views_public_metrics
    url(r'^basic-viz$', views_public_metrics.view_public_visualizations, name='view_public_visualizations'),

    url(r'^basic-viz/last12$', views_public_metrics.view_public_visualizations_last12, name='view_public_visualizations_last12'),

    url(r'^basic-viz/last12-dataverse-org$',
        views_public_metrics.view_public_visualizations_last12_dataverse_org, name='view_public_visualizations_last12_dataverse_org'),

    url(r'^files/types$',
        views_public_metrics.view_files_by_type,
        name='view_files_by_type'),

    url(r'^files/extensions$',
        views_public_metrics.view_file_extensions_within_type,
        name='view_file_extensions_within_type'),

    url (r'^unknown-content-types$',
         views_maintenance.view_files_extensions_with_unknown_content_types, name="view_files_extensions_with_unknown_content_types"),

    url (r'^all-extension-counts$',
         views_maintenance.view_all_file_extension_counts,
         name="view_all_file_extension_counts"),

    url (r'^fix-extension$',
         views_maintenance.view_fix_extension,
         name="view_fix_extension"),

    # views_test
    url(r'^metrics-links$',
        views_test.view_metrics_links,
        name='view_metrics_links'),

    url(r'^dv-tree$',
        views_test.view_dataverse_tree,
        name='view_dataverse_tree'),

    url(r'^dv-tree2$',
        views_test.view_dataverse_tree2,
        name='view_dataverse_tree2'),

    url(r'^dv-tree.json$',
        views_test.get_dataverse_tree_json,
        name='get_dataverse_tree_json'),

    url(r'^dv-tree-full.json$',
        views_test.get_dataverse_full_tree_json, name='get_dataverse_full_tree_json'),

    #url(r'^view-bins$', views_test.view_file_bins_by_datasetversion, name='view_file_bins_by_datasetversion'),


]


urlpatterns += [

    # swagger
    #url(r'^v1/swagger-test.yaml$', views_swagger_spec.view_swagger_spec_test, name='view_swagger_spec_test'),

    url(r'^v1/swagger.yaml$', views_swagger_spec.view_dynamic_swagger_spec, name='view_dynamic_swagger_spec'),

    # API endpoints
    #

    # Dataverses
    url(r'^v1/dataverses/count$', DataverseTotalCounts.as_view(), name='view_dataverse_counts'),

    url(r'^v1/dataverses/count/monthly$', DataverseCountByMonthView.as_view(), name='view_dataverse_counts_by_month'),

    url(r'^v1/dataverses/count/by-affiliation$', DataverseAffiliationCounts.as_view(), name='view_dataverse_counts_by_affiliation'),

    url(r'^v1/dataverses/count/by-type$', DataverseTypeCounts.as_view(), name='view_dataverse_counts_by_type'),



    # Datasets
    url(r'^v1/datasets/count$', DatasetTotalCounts.as_view(), name='view_dataset_counts'),

    url(r'^v1/datasets/count/monthly$', DatasetCountByMonthView.as_view(), name='view_dataset_counts_by_month'),

    url(r'^v1/datasets/count/by-subject$', DatasetSubjectCounts.as_view(), name='view_dataset_counts_by_subject'),

    url(r'^v1/datasets/file-stats$', FilesPerDatasetStats.as_view(), name='view_files_per_dataset_stats'),

    url(r'^v1/datasets/bytes-used$', BytesPerDatasetStats.as_view(), name='view_bytes_per_dataset_stats'),



    # Files
    url(r'^v1/files/count$', FileTotalCountsView.as_view(), name='view_files_counts_by_month'),

    url(r'^v1/files/count/monthly$', FileCountByMonthView.as_view(), name='view_files_counts_by_month'),

    url(r'^v1/files/count/by-type$', FileCountsByContentTypeView.as_view(), name='view_files_counts_by_type'),

    url(r'^v1/files/downloads/count/monthly$', FilesDownloadedByMonthView.as_view(), name='view_file_download_counts_by_month'),

    url(r'^v1/files/extensions$', FileExtensionsWithinContentType.as_view(), name='view_file_extensions_within_type'),

    # Test: Dataverses
    url(r'^v1/dataverses/by-id/(?P<dv_id>\d+)$', DataverseByIdView.as_view(),
    name='view_dataverse_by_id_api'),

    url(r'^v1/dataverses/by-alias/(?P<alias>[-\w]{1,255})$', DataverseByAliasView.as_view(),
    name='view_dataverse_by_alias_api'),

    # Test: Datasets
    url(r'^v1/datasets/by-id/(?P<ds_id>\d+)$', DatasetByIdView.as_view(),
    name='view_dataset_by_id_api'),

    url(r'^v1/datasets/by-persistent-id$', DatasetByPersistentIdView.as_view(),
    name='view_dataset_by_persistent_id_api'),


]

urlpatterns += [

    url(r'^test-404$', views_error_test.view_test_404, name='view_test_404'),


    url(r'^test-500$', views_error_test.view_test_500, name='view_test_500'),

]



urlpatterns += [
    url(r'^fsize$', views_test.view_bin_size,
name='view_bin_size'),
]
