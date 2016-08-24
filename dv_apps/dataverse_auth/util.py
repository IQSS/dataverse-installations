"""Convenience methods for API tokens, etc"""

from dv_apps.dataverse_auth.models import ApiToken

def is_apikey_valid(apikey):
    """Check if an apikey is valid"""

    if not apikey:
        return False, "The API key cannot be blank."

    # Is this an actual api token?
    try:
        api_info = ApiToken.objects.get(tokenstring=apikey)
    except ApiToken.DoesNotExist:
        return False, "That API key does not exist."

    # Has it expired?
    if api_info.is_expired():
        return False, "Sorry! Your API key is expired. "

    return True, None
