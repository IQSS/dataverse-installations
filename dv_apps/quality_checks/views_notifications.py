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
