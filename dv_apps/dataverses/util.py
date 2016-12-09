from django.conf import settings
from django.core.urlresolvers import reverse

class DataverseUtil(object):

    # Dataverse base url (e.g. for adding aliases)
    URL_BASE = '%s/dataverse' % settings.DATAVERSE_INSTALLATION_URL

    @staticmethod
    def get_dataverse_link(alias):
        """
        Format a link to this Dataverse
        """
        if alias is None:
            return 'Error: No alias found'
        return '%s/%s' % (DataverseUtil.URL_BASE, alias)

    @staticmethod
    def get_dataverse_serialization_link(alias):
        """
        Format a link to this Dataverse
        """
        if alias is None:
            return None

        url_path = reverse('view_dataverse_by_alias_api',\
            kwargs=dict(alias=alias))

        return '%s://%s%s' % (settings.SWAGGER_SCHEME,\
                settings.SWAGGER_HOST,\
                url_path)
