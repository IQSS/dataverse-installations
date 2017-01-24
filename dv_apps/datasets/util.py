from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.utils import query_helper

def get_latest_dataset_version(dataset_id):
    """Given a dataset id, retrieve the latest *published* DatasetVersion"""

    dataset = Dataset.objects.select_related('dvobject'\
            ).filter(dvobject__id=dataset_id\
            ).filter(**query_helper.get_is_published_filter_param()\
            ).first()

    if dataset is None:
        return None

    # Get the latest version
    dataset_version = DatasetVersion.objects\
            .select_related('dataset')\
            .filter(dataset=dataset,\
                versionstate=VERSION_STATE_RELEASED)\
            .order_by('-id').first()

    return dataset_version
