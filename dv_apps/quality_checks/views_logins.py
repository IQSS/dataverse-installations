from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404
from dv_apps.dataverse_auth.util_logins import UserLoginInfo,\
                                               MonthlyNewUserStats,\
                                               NEW_USER_START_YEAR
from django.views.decorators.cache import cache_page
from datetime import datetime as dt

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_recent_logins(request):
    """View details about broken notifications"""

    user_login_stats = [UserLoginInfo(num_days=7),
                        UserLoginInfo(num_days=30),
                        UserLoginInfo(num_days=100),
                        ]

    info_dict = dict(page_title="Recent User Logins/API Use",
                     user_login_stats=user_login_stats,
                     )

    return render(request,
                  'view_recent_logins.html',
                  info_dict)

#@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_new_user_counts(request, selected_year=None):
    """View new users for a given year"""
    time_now = dt.now()

    if selected_year is None or (not str(selected_year).isdigit()):
        selected_year = time_now.year

    selected_year = int(selected_year)
    if selected_year < NEW_USER_START_YEAR:
        selected_year = time_now.year
    elif selected_year > time_now.year:
        selected_year = time_now.year



    new_user_stats = MonthlyNewUserStats(selected_year=selected_year)

    info_dict = dict(page_title="New Users By Month",
                     new_user_stats=new_user_stats,
                     year_menu=range(NEW_USER_START_YEAR, time_now.year+1),
                     selected_year=new_user_stats.selected_year)

    return render(request,
                  'view_new_users.html',
                  info_dict)
