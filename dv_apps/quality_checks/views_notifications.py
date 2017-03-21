from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from dv_apps.quality_checks.util_notifications import NotificationStats
from dv_apps.quality_checks.util_content_types import ContentTypeStats
from django.views.decorators.cache import cache_page


def view_broken_notifications(request):
    """View details about broken notifications"""

    notice_stats = NotificationStats()

    info_dict = dict(page_title="Broken Notifications",
                     broken_info_list=notice_stats.broken_info_list,
                     #df_first_created=df_first_created,
                     #df_last_created=df_last_created,
                     #num_datasets=num_datasets,
                     subtitle='Broken Notfications',
                     installation_url=settings.DATAVERSE_INSTALLATION_URL,
                     )

    return render(request,
                  'broken_notifications.html',
                  info_dict)


def view_broken_notification_details(request, model_name):
    """View broken notification details about a particular model/object types
    Example: broken notifications related to a Dataverse"""
    if not request.user.is_authenticated():
        return HttpResponse('You have to be logged in')
    if not request.user.is_superuser:
        return HttpResponse('You don\'t have permission')


    assert model_name is not None, "model_name cannot be None"

    model_name = model_name.strip()

    notice_stats = NotificationStats(**dict(selected_model_name=model_name))

    info_dict = dict(page_title="Broken Notifications for %s" % model_name,
                     broken_info_list=notice_stats.broken_info_list,
                     subtitle='Broken Notfications for %s' % model_name,
                     installation_url=settings.DATAVERSE_INSTALLATION_URL,
                     )

    return render(request,
                  'broken_notification_details.html',
                  info_dict)
