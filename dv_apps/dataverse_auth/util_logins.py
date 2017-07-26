"""
Convenience class for counting the number of users who recently logged in
"""
from dv_apps.dataverse_auth.models import AuthenticatedUser
#from dv_apps.utils.msg_util import msg, msgt
#from collections import Counter
from datetime import datetime, timedelta


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
