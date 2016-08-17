"""
This router sends django-specific tables to another db.

For these circumstances:
    -  We want to explore an existing relational database using Django, including the admin.
    -  We don't want to add any django-specific tables to the existing dastabase.

Based on: https://docs.djangoproject.com/en/1.9/topics/db/multi-db/#database-routers
"""

APPS_TO_ROUTE = [ 'auth', 'contenttypes', 'sessions', 'sites', 'admin', 'installations', 'migrations']
DB_REFERENCE_NAME = 'dataverse'

def is_dataverse_app_to_route(app_label):
    """If the app is not in the list:
        - Assume it's a Dataverse app
        - Route it
    """
    if app_label in APPS_TO_ROUTE:
        return False
    return True

'''def is_django_app_to_route(app_label):
    """Should we route this app?"""
    if app_label in APPS_TO_ROUTE:
        return True
    return False
'''

class DataverseRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if is_dataverse_app_to_route(model._meta.app_label):
            return DB_REFERENCE_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if is_dataverse_app_to_route(model._meta.app_label):
            return DB_REFERENCE_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if is_dataverse_app_to_route(obj1._meta.app_label) or \
           is_dataverse_app_to_route(obj2._meta.app_label):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if is_dataverse_app_to_route(app_label):
            return db == DB_REFERENCE_NAME
        return None
