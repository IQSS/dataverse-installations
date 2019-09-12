from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

#from dv_apps.installations.models import Installation, Institution
from collections import OrderedDict
import json
from installations.models import Installation


from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def index(request):
    return HttpResponse("Hello, world. You're at the installations index.")

#@cache_page(get_metrics_cache_time())
def view_installations_json_pretty(request):

    return view_installations_json(request, True)

#@cache_page(get_metrics_cache_time())
def view_installations_json(request, pretty=False):

    l = Installation.objects.all()

    dv_list = [dv.to_json() for dv in l]

    installations_dict =  object_pairs_hook=OrderedDict(installations=dv_list)
    #content = json.dumps(installations_dict)
    content = json.dumps(installations_dict, cls=DecimalEncoder)
    #content = json.dumps(installations_dict, use_decimal=True)
    return HttpResponse(content,

    #print 'pretty', pretty
    #if pretty:
    #    content = '<html><pre>%s</pre></html>' %\
    #              json.dumps(installations_dict,
    #                         indent=4)
    #    return HttpResponse(content)
    #else:
    #    content = json.dumps(installations_dict)
    #    return HttpResponse(content,
                            content_type="application/json")
