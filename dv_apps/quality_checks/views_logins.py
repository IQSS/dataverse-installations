from django.shortcuts import render
from django.http import HttpResponse, Http404
from dv_apps.dataverse_auth.util_logins import UserLoginInfo
from django.views.decorators.cache import cache_page


def view_recent_logins(request):
    """View details about broken notifications"""

    user_login_stats = [UserLoginInfo(num_days=7),
                        UserLoginInfo(num_days=30),
                        UserLoginInfo(num_days=100),
                        ]


    info_dict = dict(page_title="Recent User Logins/API Use",
                     user_login_stats=user_login_stats,
                     xsubtitle='Broken Notfications')

    return render(request,
                  'view_recent_logins.html',
                  info_dict)
