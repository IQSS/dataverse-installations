from django.conf import settings

TWO_HOURS_IN_SECONDS = 60 * 60 * 2

def get_metrics_cache_time():
    if settings.METRICS_CACHE_VIEW:
        return settings.METRICS_CACHE_VIEW_TIME
        # return TWO_HOURS_IN_SECONDS
    else:
        return 0
