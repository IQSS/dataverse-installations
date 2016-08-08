from django.conf.urls import url
#from dv_apps.metrics.views import view_dataset_count
from dv_apps.metrics import views, views_test, views_public_metrics


REGEX_YYYY_MM_DD = '\d{4}-\d{1,2}-\d{1,2}'
#REGEX_YYYY_MM_DD = '(19|20)\d{2}-\d{1,2}-\d{1,2}'



urlpatterns = [

    # views_public_metrics
    url(r'^basic-viz$', views_public_metrics.view_public_visualizations, name='view_public_visualizations'),

    url(r'^basic-viz/last12$', views_public_metrics.view_public_visualizations_last12, name='view_public_visualizations_last12'),

    url(r'^files/types$', views_public_metrics.view_files_by_type, name='view_files_by_type'),

    url(r'^files/extensions$', views_public_metrics.view_file_extensions_within_type, name='view_file_extensions_within_type'),

    # views_test
    url(r'^dv-tree$', views_test.view_dataverse_tree, name='view_dataverse_tree'),

    #url(r'^datasets/count/simple$', views_api.view_simple_dataset_count, name='view_simple_dataset_count'),

    url(r'^datasets/count/simple2$', views.view_simple_dataset_count2, name='view_simple_dataset_count2'),

    #url(r'^datasets/count$', views_api.view_dataset_count, name='view_dataset_count'),

    #url(r'^datasets/count/jcabanas$', views_api.view_jcabanas, name='view_jcabanas'),

    #url(r'^datasets/count-by-month$', views_api.view_dataset_counts_by_month, name='view_dataset_counts_by_month'),



]
