"""
Defines a decorator that checks for an unexpired API KEY
when settings.DEBUG=False

9/6/16 - hasty addition of superuser_apikey_required, need to factor out..
"""

#from functools import wraps
from django.http import JsonResponse, QueryDict
from django.conf import settings
from django.views.decorators.cache import cache_page

from dv_apps.dataverse_auth.util import is_apikey_valid, is_apikey_valid_superuser

#cache_page(get_metrics_cache_time())


API_ERR_MSG_KEY = 'API_ERR_MSG_KEY'

def bad_api_view(request, *args, **kwargs):

    err_msg = kwargs.get(API_ERR_MSG_KEY, None)
    if err_msg is None:
        err_msg = "Sorry, there was an error with your API key."

    d = dict(status='ERROR',\
            message=err_msg)
    return JsonResponse(d)

PARAM_NAME_KEY = 'key'  # URL parameter for api key

def apikey_required(view_func):
    """View wrapper.  Dataverse API key required if DEBUG=False"""

    def check_apikey(request, *args, **kwargs):

        # maybe do something before the view_func call
        # that uses `extra_value` and the `request` object
        if settings.DEBUG is False:

            # ---------------------------
            # Assume production, check the API key
            # ---------------------------
            api_key = request.GET.get(PARAM_NAME_KEY, None)
            if api_key is not None:
                api_key = api_key.strip()

            # ---------------------------
            # Has an API key been specified?
            # ---------------------------
            if api_key is None:
                error_message = ("A Dataverse API key is required."
                    " Please see"
                    " http://guides.dataverse.org/en/latest/api/native-api.html")
                kwargs[API_ERR_MSG_KEY] = error_message
                return bad_api_view(request, *args, **kwargs)

            # ---------------------------
            # Is the API key valid?
            # ---------------------------
            success, err_msg_or_none = is_apikey_valid(api_key)
            if not success:
                kwargs[API_ERR_MSG_KEY] = err_msg_or_none
                return bad_api_view(request, *args, **kwargs)

        # ---------------------------
        # OK, Continue on!
        # ---------------------------
        response = view_func(request, *args, **kwargs)

        # (maybe do something after the view_func call)
        #
        return response

    return check_apikey



def superuser_apikey_required(view_func):
    """View wrapper.  Dataverse API key required if DEBUG=False"""

    def check_superuser_apikey(request, *args, **kwargs):

        # maybe do something before the view_func call
        # that uses `extra_value` and the `request` object
        if settings.DEBUG is False:

            # ---------------------------
            # Assume production, check the API key
            # ---------------------------
            api_key = request.GET.get(PARAM_NAME_KEY, None)
            if api_key is not None:
                api_key = api_key.strip()

            # ---------------------------
            # Has an API key been specified?
            # ---------------------------
            if api_key is None:
                error_message = ("A Dataverse API key is required."
                    " Please see"
                    " http://guides.dataverse.org/en/latest/api/native-api.html")
                kwargs[API_ERR_MSG_KEY] = error_message
                return bad_api_view(request, *args, **kwargs)

            # ---------------------------
            # Is the API key valid?
            # ---------------------------
            success, err_msg_or_none = is_apikey_valid_superuser(api_key)
            if not success:
                kwargs[API_ERR_MSG_KEY] = err_msg_or_none
                return bad_api_view(request, *args, **kwargs)

        # ---------------------------
        # OK, Continue on!
        # ---------------------------
        response = view_func(request, *args, **kwargs)

        # (maybe do something after the view_func call)
        #
        return response

    return check_superuser_apikey
"""
to_dict = dict(request.GET.iterlists())
to_dict.pop(PARAM_NAME_KEY)
qdict = QueryDict('', mutable=True)
qdict.update(to_dict)
request.GET = qdict
"""
