from django.shortcuts import render
from django.views.decorators.cache import cache_page

from dv_apps.installations.models import Installation, Institution
from dv_apps.utils.metrics_cache_time import get_metrics_cache_time

from dv_apps.metrics.stats_count_util import get_total_published_counts

@cache_page(get_metrics_cache_time())
def view_map(request):
    """Show Dataverse map with affiliated Institutions"""

    # Retrieve the installations
    install_list = Installation.objects.all()
    arr = []

    # For each Installation, add the affiliated Institutions
    for i  in install_list:
        lists = Institution.objects.filter(host__name=i.name)
        arr.append(lists)

    d = dict(
        install_list = install_list,
        arr = arr,
    )

    d.update(get_total_published_counts())
    print get_total_published_counts()
    return render(request, 'installations/map.html', d)
