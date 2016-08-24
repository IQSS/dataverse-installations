from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from dv_apps.dataverse_auth.util import is_apikey_valid



def apikey_required(view_func):
    """View wrapper.  Dataverse API key required if DEBUG=False"""

    def decorator(request, *args, **kwargs):

        # maybe do something before the view_func call
        # that uses `extra_value` and the `request` object
        if 1:#settings.DEBUG is False:

            # Assume production, check the API key
            api_key = request.GET.get('key', None)

            # Has an API key been specified?
            if api_key is None:
                error_message = ("A Dataverse API key is required."
                    " Please see"
                    " http://guides.dataverse.org/en/latest/api/native-api.html")
                return JsonResponse(status="ERROR",\
                        error_message=error_message)

            # Is the API key valid?
            success, err_msg_or_none = is_apikey_valid(api_key)
            if not success:
                return JsonResponse(status="ERROR",\
                    error_message=err_msg_or_none)

        # OK, Continue on!
        response = view_func(request, *args, **kwargs)

        # maybe do something after the view_func call
        #
        return response

    return decorator
