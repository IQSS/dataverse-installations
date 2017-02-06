"""
Hanlde Slack channel requests
"""
from django.conf.urls import url
from dv_apps.slackbot import views

urlpatterns = (

    url(r'^incoming$', views.view_handle_incoming, name='view_handle_incoming'),

    url(r'^incoming-test$', views.view_test_slack_hook, name='view_test_slack_hook'),

)
