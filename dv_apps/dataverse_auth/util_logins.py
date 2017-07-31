"""
Convenience class for counting the number of users who recently logged in
"""
from dv_apps.dataverse_auth.models import AuthenticatedUser
from django.db.models import Q
import calendar
from datetime import datetime, timedelta

NEW_USER_START_YEAR = 2017 # year when user created time became available

class MonthlyNewUserInfo(object):
    """Place holder for new user stats"""
    def __init__(self, selected_year, month_num):

        assert str(selected_year).isdigit(), "selected_year must be an integer"
        assert str(month_num).isdigit(), "month_num must be an integer"
        assert month_num >= 1 and month_num <= 12, "month_num must be an integer between 1 and 12"

        self.selected_year = selected_year
        self.month_num = month_num
        self.label = calendar.month_name[month_num]

        self.total_users = 0
        self.total_hu_users = 0
        self.total_non_hu_users = 0

        self.monthly_new_users = 0
        self.monthly_hu_new_users = 0
        self.monthly_non_hu_new_users = 0

        self.gather_info()

    def gather_info(self):

        hu_params = Q(email__icontains='harvard.') | Q(affiliation__icontains='harvard')

        # the given month and prior
        time_params = dict(createdtime__year__lte=self.selected_year,
                           createdtime__month__lte=self.month_num)

        self.total_users = AuthenticatedUser.objects.filter(**time_params).count()
        self.total_hu_users = AuthenticatedUser.objects.filter(hu_params\
                                ).filter(**time_params).count()

        # calculate non hu users
        self.total_non_hu_users = self.total_users - self.total_hu_users

        # only the given month
        time_params2 = dict(createdtime__year=self.selected_year,
                            createdtime__month=self.month_num)

        self.monthly_new_users = AuthenticatedUser.objects.filter(**time_params2).count()

        self.monthly_hu_new_users = AuthenticatedUser.objects.filter(hu_params\
                                ).filter(**time_params2\
                                ).count()

        self.monthly_non_hu_new_users = self.monthly_new_users - self.monthly_hu_new_users


class MonthlyNewUserStats(object):

    def __init__(self, **kwargs):
        """
        num_days = how many days back from today to count users who logged in
        """
        self.selected_year = kwargs.get('selected_year', datetime.now().year)
        assert str(self.selected_year).isdigit(), "selected_year must be an integer"

        self.time_now = datetime.now()
        self.monthly_user_counts = []
        #self.annual_new_users = 0

        self.calculate_new_users()

    def calculate_new_users(self):
        """Calculate new user info for the given year"""

        for month_num in range(1, 13):

            # has the month happened yet?
            if self.selected_year == self.time_now.year\
                and month_num > self.time_now.month:
                continue    # skip it, this month is in the future

            mth_user_info = MonthlyNewUserInfo(self.selected_year, month_num)

            self.monthly_user_counts.append(mth_user_info)

        #self.annual_new_users = sum([x.monthly_new_users\
        #                             for x in self.monthly_user_counts])



class UserLoginInfo(object):
    """Count the number of users who
    recently logged in or used their API keys"""

    def __init__(self, **kwargs):
        """
        num_days = how many days back from today to count users who logged in
        """
        self.num_days = kwargs.get('num_days', 10)
        assert str(self.num_days).isdigit(), "num_days must be an integer"

        self.start_date = datetime.now() - timedelta(days=self.num_days)

        self.cnt_logins = 0
        self.cnt_apikey_use = 0
        self.total_count = 0

        self.calculate_login_info()


    def calculate_login_info(self):

        self.cnt_logins = AuthenticatedUser.objects.filter(\
                            lastlogintime__gte=self.start_date).count()

        self.cnt_apikey_use = AuthenticatedUser.objects.filter(\
                            lastapiusetime__gte=self.start_date).count()

        self.total_count = self.cnt_logins + self.cnt_apikey_use
