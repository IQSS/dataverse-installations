from django.conf.urls import url
from .views import view_list_datasets, view_dataset_detail

urlpatterns = (
    url(r'^list/?', view_list_datasets, name='view_list_datasets'),
    url(r'^view/(?P<dataset_id>\d{1,8})?', view_dataset_detail, name='view_dataset_detail'),
    #url(r'^t/(?P<username>\w{1,50})', 'view_test_query', name='view_test_query_with_username'),

    #url(r'^test-query', 'view_test_query', name='view_test_query'),

 #   url(r'^send-metadata-to-dataverse/(?P<import_success_id>\d{1,10})/$', 'send_metadata_to_dataverse', name="send_metadata_to_dataverse"),

  #  url(r'^params-for-datavarse/(?P<import_success_id>\d{1,10})/$', 'show_import_success_params', name="show_import_success_params"),

)
