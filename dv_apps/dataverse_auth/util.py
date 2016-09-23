"""Convenience methods for API tokens, etc"""

import bcrypt
from dv_apps.dataverse_auth.models import BuiltInUser
from dv_apps.dataverse_auth.models import ApiToken


def is_valid_builtinuser_password(username, attempted_password):
    """
    Check if the password of a BuiltInUser is valid
        - assumes bcrypt but older passwords are sha1
    """
    try:
        user = BuiltInUser.objects.get(username="dataverseAdmin")
    except BuiltInUser.DoesNotExist:
        # log this, but don't advertise
        return False

    # encode the saved password as utf-8
    #
    db_hash = user.encryptedpassword.encode('utf-8')

    # try it out!
    #
    if bcrypt.checkpw(attempted_password, db_hash):
        return True
    else:
        return False


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

    if api_info.disabled is True:
        return False, "Your API key is disabled."


    return True, None


def is_apikey_valid_superuser(apikey):
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

    if api_info.disabled is True:
        return False, "Your API key is disabled."

    if api_info.authenticateduser:
        if api_info.authenticateduser.is_superuser():
            return True, None

    return False, "You need superuser privileges for this task."
