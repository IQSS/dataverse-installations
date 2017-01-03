import json
from os import path
from collections import OrderedDict

from django.shortcuts import render
from django.http import Http404#, HttpResponse
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from django.conf import settings

from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.datasets.util import get_latest_dataset_version
from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer
from django.views.decorators.cache import cache_page

from dv_apps.datasets.serializer import DatasetSerializer

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django.template.loader import get_template, TemplateDoesNotExist

PARAM_TEMPLATE_NAME = 'tmpl'

TEMPLATE_DICT = OrderedDict({
    'breadcrumb.html' : 'Breadcrumb',
    'dataverse_theme.html' : 'Dataverse Theme',
    'title_citation.html' : 'Title/Citation',
})

def view_side_by_side1_by_persistent_id(request):

    persistent_id = request.GET.get('persistentId', None)
    if persistent_id is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    ds = Dataset.get_dataset_by_persistent_id(persistent_id)
    if ds is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    return view_side_by_side1(request, ds.id)

def view_side_by_side1(request, dataset_id):

    dsv = get_latest_dataset_version(dataset_id)
    if dsv is None:
        raise Http404("No published datasets for id: %s" % dataset_id)

    template_basename = request.GET.get(PARAM_TEMPLATE_NAME, 'title_citation.html')
    template_fname = path.join('dvobject_api', template_basename)

    try:
        template = get_template(template_fname)
    except TemplateDoesNotExist:
        raise Http404('Template does not exist: %s' % template_fname)

    #formatter = HtmlFormatter(linenos=True, cssclass="friendly")
    formatter = HtmlFormatter(linenos=False, cssclass="friendly")

    # -------------------------------
    # Format raw template
    # -------------------------------
    template_html = open(template.origin.name, 'r').read()
    django_lexer = get_lexer_by_name("django", stripall=True)
    template_snippet = highlight(template_html, django_lexer, formatter)
    template_name = path.basename(template.origin.name)

    # -------------------------------
    # Format Dataset JSON
    # -------------------------------
    dataset_dict = DatasetSerializer(dsv).as_json()

    citation_block=dataset_dict.get('metadata_blocks', {}).get('citation')
    #citation_dict = OrderedDict({'citation_block': citation_block})
    json_string = json.dumps(dataset_dict, indent=4)

    json_lexer = get_lexer_by_name("json", stripall=True)
    dataset_json_snippet = highlight(json_string, json_lexer, formatter)

    # -------------------------------
    # Format Dataverse JSON
    # -------------------------------
    dataverse_id = dataset_dict['ownerInfo']['id']
    try:
        dataverse = Dataverse.objects.select_related('dvobject')\
                    .get(dvobject__id=dataverse_id)
    except Dataverse.DoesNotExist:
        raise Http404('No Dataverse with id: %s' % dataverse_id)

    dataverse_dict = DataverseSerializer(dataverse).as_json()
    #dataset_json_snippet = highlight(json_string, json_lexer, formatter)

    # -------------------------------
    # Overall pygment css
    # -------------------------------
    pygment_css = formatter.get_style_defs('.friendly')

    # -------------------------------
    # API endpoint
    # -------------------------------
    swagger_base_url = '%s://%s' % (settings.SWAGGER_SCHEME, settings.SWAGGER_HOST)


    lu = dict(template_snippet=template_snippet,
            template_name=template_name,
            dataset_json_snippet=dataset_json_snippet,
            pygment_css=pygment_css,
            swagger_base_url=swagger_base_url,
            dataset_id=dataset_id,
            ds=dataset_dict,                # for rendering chosen template
            citation_block=citation_block, # for rendering chosen template
            )

    lu['rendered_template'] = render_to_string(template_fname, lu)

    return render(request, 'composable/side_by_side.html', lu)
