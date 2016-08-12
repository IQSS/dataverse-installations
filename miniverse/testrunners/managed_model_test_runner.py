"""
Used to create a test database when using unmanaged models.
See gist: https://gist.github.com/raprasad/f292f94657728de45d1614a741928308
Also, see this post (including comments):
 http://blog.birdhouse.org/2015/03/25/django-unit-tests-against-unmanaged-databases/
"""
from django.test.runner import DiscoverRunner
from django.apps import apps


class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    """
    def setup_test_environment(self, *args, **kwargs):

        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]

        for m in self.unmanaged_models:
            m._meta.managed = True


        #import ipdb; ipdb.set_trace()
        super(ManagedModelTestRunner, self).setup_test_environment(*args,
                                                                   **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelTestRunner, self).teardown_test_environment(*args,
                                                                      **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False
