import json
from django.shortcuts import render
from django.http import HttpResponse    #JsonResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dv_apps.dvobject_api.views_dataverses import view_get_slack_dataverse_info
from dv_apps.dvobject_api.views_datasets import view_get_slack_dataset_info
from dv_apps.dvobjects.models import DvObject

@require_POST
@csrf_exempt
def view_handle_incoming(request):

    if request.POST.get('token') == settings.SLACK_WEBHOOK_SECRET:
        #channel = request.POST.get('channel_name')
        #username = request.POST.get('user_name')
        #inbound_message = '%s in channel %s says `%s`' %\
        #                (username, channel, text)
        #print(inbound_message)

        text = request.POST.get('text')
        resp_dict = dict(text=parse_message(text))
        return HttpResponse(json.dumps(resp_dict))



    else:
        return HttpResponse('no slack')
    #SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET').SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEB

def parse_message(slack_text):

    slack_text = slack_text.strip()

    slack_items = slack_text.split()

    if len(slack_items) > 1 and not slack_items[1].isdigit():
        return get_help_text()

    dvobject_id = slack_items[1]
    try:
        dvobject = DvObject.objects.get(pk=dvobject_id)
    except:
        return "No DvObject with id: %s" % dvobject_id


    if len(slack_items) >= 3:
        extra_args = { slack_items[2] : True }
    else:
        extra_args = {}

    if dvobject.dtype == 'Dataverse':
        return view_get_slack_dataverse_info(dvobject.id) +\
                "\nIt's a Dataverse!"

    elif dvobject.dtype == 'Dataset':
        return view_get_slack_dataset_info(dvobject.id, **extra_args)
    else:
        return "It's a %s" % dvobject.dtype


    #return 'looks good'


def get_help_text():
    return """```
Commands for dvbot (only on test db)

# Return a Dataverse in JSON
dv [dataverse id]
```"""


def view_test_slack_hook(request):

    return HttpResponse('It works!')
