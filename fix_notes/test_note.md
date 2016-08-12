gist: https://gist.github.com/raprasad/f292f94657728de45d1614a741928308

## Scenario
  - Django 1.9 application with two databases:
    - Legacy database with readonly access--[unmanaged models](https://docs.djangoproject.com/en/1.9/ref/models/options/#managed).  Both Django models (models.py) and related migrations have "managed" set to ```False```
      - ```'managed': False```
    - Default database holding django specific tables (e.g. auth_user, django_content_type, etc)

## Testing Woes
  - For testing I want to re-create the legacy database tables.  In other words, during ```python manage.py test```, tell Django to set "managed" to ```True```
    - There are several excellent blog posts on how to do this *without migrations*, especially:
      - http://blog.birdhouse.org/2015/03/25/django-unit-tests-against-unmanaged-databases/
  - However, I was still hitting errors becauuse of the migrations.  Comments in the blog post above led me to this gist:
    - https://gist.github.com/NotSqrt/5f3c76cd15e40ef62d09
  - Also, the [django-test-without-migrations](https://pypi.python.org/pypi/django-test-without-migrations/) package didn't seem to be working/recently updated  

## Combining the blog post and gist above gave the following which is working!

Thanks to [Scot Hacker](http://blog.birdhouse.org/2015/03/25/django-unit-tests-against-unmanaged-databases/) and @NotSqrt who wrote this code:

```python
from project.local_settings import *
from django.test.runner import DiscoverRunner

class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

class UnManagedModelTestRunner(DiscoverRunner):
    '''
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run.
    Many thanks to the Caktus Group: http://bit.ly/1N8TcHW
    '''

    def setup_test_environment(self, *args, **kwargs):
        from django.db.models.loading import get_models
        self.unmanaged_models = [m for m in get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False

# Since we can't create a test db on the read-only host, and we
# want our test dbs created with postgres rather than the default, override
# some of the global db settings, only to be in effect when "test" is present
# in the command line arguments:

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage

    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['USER'] = 'username'
    DATABASES['default']['PASSWORD'] = 'secret'

    DATABASES['tmi']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['tmi']['HOST'] = '127.0.0.1'
    DATABASES['tmi']['USER'] = 'username'
    DATABASES['tmi']['PASSWORD'] = 'secret'


# The custom routers we're using to route certain ORM queries
# to the remote host conflict with our overridden db settings.
# Set DATABASE_ROUTERS to an empty list to return to the defaults
# during the test run.
DATABASE_ROUTERS = []

# Skip the migrations by setting "MIGRATION_MODULES"
# to the DisableMigrations class defined above
#
MIGRATION_MODULES = DisableMigrations()

# Set Django's test runner to the custom class defined above
TEST_RUNNER = 'project.test_settings.UnManagedModelTestRunner'

```
