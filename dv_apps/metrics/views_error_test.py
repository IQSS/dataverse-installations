"""
Endpoints to purposely throw 404 and 500 errors
For testing emails to ADMINS and MANAGERS
"""
from django.http import HttpResponse, Http404


def view_test_404(request):
    """Used to test auto emails from Django's BrokenLinkEmailsMiddleware
    See docs here: https://docs.djangoproject.com/en/1.9/howto/error-reporting/#errors
    """
    # Uh, could just go to a page that really doesn't exist...
    raise Http404('just a test')


def view_test_500(request):
    """Used to test Django emails from a 500 error"""

    bad_medicine = 12 / 0   # div by 0 to force a 500 error

    return HttpResponse("Ain't ever gonna get here: %d" % bad_medicine)


"""
Note, to kick-off an email to the site MANAGERS, a 404 must have a referer.

Quick manual test:
```
import requests

# set referer
my_referer = 'http://www.w3.org/hypertext/DataSources/Overview.html'
# set url
url = 'https://services-dataverse.herokuapp.com/metrics/test-404'

# make url request with referer
s = requests.Session()
s.headers.update({'referer': my_referer})
s.get(url)
```
"""
