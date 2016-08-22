from django.http import HttpResponse, Http404


def view_test_404(request):
    """Used to test auto emails from Django's BrokenLinkEmailsMiddleware"""
    # Uh, could just go to a page that really doesn't exist...
    raise Http404('just a test')

def view_test_500(request):
    """Used to test Django emails from a 500 error"""

    bad_medicine = 12 / 0   # div by 0 to force a 500 error

    return HttpResponse("Ain't ever gonna get here: %d" % bad_medicine)
