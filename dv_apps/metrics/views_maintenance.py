"""
Metric views, returning JSON repsonses
"""
from django.shortcuts import render
from django.views.decorators.cache import cache_page
#from django.http import JsonResponse, HttpResponse, Http404
from dv_apps.metrics.stats_util_files import StatsMakerFiles, FILE_TYPE_OCTET_STREAM
from dv_apps.utils.metrics_cache_time import get_metrics_cache_time
from dv_apps.metrics.forms import FixContentTypeForm

FIVE_HOURS = 60 * 60 * 5

"""
from django.core.cache import cache
cache.clear()
"""

@cache_page(get_metrics_cache_time())
def view_all_file_extension_counts(request):
    """Reference table of all file extensions with counts"""

    stats_files = StatsMakerFiles()
    all_counts = stats_files.view_file_extensions_within_type()
    if all_counts and all_counts.result_data:
        d = dict(all_counts=all_counts.result_data['file_extension_counts'],
                total_file_count=all_counts.result_data['total_file_count'],
                number_unique_extensions=all_counts.result_data['number_unique_extensions'],
                )
    else:
        d = dict(all_counts=[],
                total_file_count=0,
                number_unique_extensions=0,
                )

    return render(request, 'metrics/view_all_file_extension_counts.html', d)


@cache_page(get_metrics_cache_time())
def view_files_extensions_with_unknown_content_types(request):
    """Reference table of file extensions with unkown content type"""

    stats_files = StatsMakerFiles()
    unknown_counts = stats_files.view_file_extensions_within_type(FILE_TYPE_OCTET_STREAM)
    if unknown_counts and unknown_counts.result_data:
        d = dict(unknown_counts=unknown_counts.result_data['file_extension_counts'],
                total_file_count=unknown_counts.result_data['total_file_count'],
                number_unique_extensions=unknown_counts.result_data['number_unique_extensions'],
                all_dv_files_count=unknown_counts.result_data['all_dv_files'],
                percent_unknown=unknown_counts.result_data['percent_unknown'])
    else:
        d = dict(unknown_counts=[],
                total_file_count=0,
                number_unique_extensions=0,
                all_dv_files_count=0,
                percent_unknown=0)

    return render(request, 'metrics/view_file_extensions_with_unknown_content_types.html', d)

def view_fix_extension(request):

    d = {}
    if request.POST:
        f = FixContentTypeForm(request.POST)
        if f.is_valid():
            d['fix_instructions'] = f.get_fix_instructions()
            #f = FixContentTypeForm()
    else:
        if request.GET.has_key('ext'):
            initial_data = dict(file_extension=request.GET['ext'])
        else:
            initial_data = {}
        f = FixContentTypeForm(initial=initial_data)

    d['fix_form'] = f

    return render(request, 'metrics/maintenance/view_fix_extension.html', d)
