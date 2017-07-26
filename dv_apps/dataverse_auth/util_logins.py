"""
Convenience class for counting the number of users who recently logged in
"""
from dv_apps.dataverse_auth.models import AuthenticatedUser
#from dv_apps.utils.msg_util import msg, msgt
import calendar
from datetime import datetime, timedelta

class MonthlyNewUserStats(object):

    def __init__(self, **kwargs):
        """
        num_days = how many days back from today to count users who logged in
        """
        self.selected_year = kwargs.get('selected_year', datetime.now().year)
        assert str(self.selected_year).isdigit(), "selected_year must be an integer"

        self.monthly_new_users = []
        self.total_new_users = 0
        self.calculate_new_users()

    def calculate_new_users(self):

        for month_num in range(1, 13):
            label = '%s %s' % (calendar.month_name[month_num], self.selected_year)

            query_params = dict(createdtime__year=self.selected_year,
                                createdtime__month=month_num)

            cnt = AuthenticatedUser.objects.filter(**query_params).count()

            self.monthly_new_users.append((label, cnt))

        self.total_new_users = sum([x[1] for x in self.monthly_new_users])

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
