from django.conf.urls import url
#from dv_apps.metrics.views import view_dataset_count
from . import views_api


REGEX_YYYY_MM_DD = '\d{4}-\d{1,2}-\d{1,2}'
#REGEX_YYYY_MM_DD = '(19|20)\d{2}-\d{1,2}-\d{1,2}'

urlpatterns = [
    url(r'^datasets/count/simple$', views_api.view_simple_dataset_count, name='view_simple_dataset_count'),

    url(r'^datasets/count$', views_api.view_dataset_count, name='view_dataset_count'),
    
    url(r'^datasets/count/jcabanas$', views_api.view_jcabanas, name='view_jcabanas'),
    
    

    url(r'^datasets/count-by-month$', views_api.view_dataset_counts_by_month, name='view_dataset_counts_by_month'),


    #url(r'^datasets/count/(?P<start_date_str>%s)$' % REGEX_YYYY_MM_DD, views_api.view_dataset_count, name='view_dataset_count_start_date'),

    #url(r'^datasets/count/(?P<start_date_str>{0})/(?P<end_date_str>{0})$'.format(REGEX_YYYY_MM_DD), views_api.view_dataset_count, name='view_dataset_count_start_end_dates'),

    #url(r'^t/(?P<username>\w{1,50})', 'view_test_query', name='view_test_query_with_username'),

    #url(r'^test-query', 'view_test_query', name='view_test_query'),

 #   url(r'^send-metadata-to-dataverse/(?P<import_success_id>\d{1,10})/$', 'send_metadata_to_dataverse', name="send_metadata_to_dataverse"),

  #  url(r'^params-for-datavarse/(?P<import_success_id>\d{1,10})/$', 'show_import_success_params', name="show_import_success_params"),

]
