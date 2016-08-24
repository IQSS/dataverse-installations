"""
Defines a decorator that checks for an unexpired API KEY
when settings.DEBUG=False
"""

#from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from dv_apps.dataverse_auth.util import is_apikey_valid

API_ERR_MSG_KEY = 'API_ERR_MSG_KEY'
def bad_api_view(request, *args, **kwargs):

    err_msg = kwargs.get(API_ERR_MSG_KEY, None)
    if err_msg is None:
        err_msg = "Sorry, there was an error with your API key."

    d = dict(status='ERROR',\
            message=err_msg)
    return JsonResponse(d)


def apikey_required(view_func):
    """View wrapper.  Dataverse API key required if DEBUG=False"""

    def check_apikey(request, *args, **kwargs):

        # maybe do something before the view_func call
        # that uses `extra_value` and the `request` object
        if settings.DEBUG is False:

            # Assume production, check the API key
            api_key = request.GET.get('key', None)

            # Has an API key been specified?
            if api_key is None:
                error_message = ("A Dataverse API key is required."
                    " Please see"
                    " http://guides.dataverse.org/en/latest/api/native-api.html")
                kwargs[API_ERR_MSG_KEY] = error_message
                return bad_api_view(request, *args, **kwargs)
                #raise Exception(error_message)

            # Is the API key valid?
            success, err_msg_or_none = is_apikey_valid(api_key)
            if not success:
                kwargs[API_ERR_MSG_KEY] = err_msg_or_none
                return bad_api_view(request, *args, **kwargs)
                #raise Exception(err_msg_or_none)

        # OK, Continue on!
        response = view_func(request, *args, **kwargs)

        # maybe do something after the view_func call
        #
        return response

    return check_apikey
