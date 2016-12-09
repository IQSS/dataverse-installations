from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED


def get_latest_dataset_version(dataset_id):
    """Given a dataset id, retrieve the latest *published* DatasetVersion"""

    try:
        dataset = Dataset.objects.select_related('dvobject').get(\
            dvobject__id=dataset_id,\
            dvobject__publicationdate__isnull=False)
    except Dataset.DoesNotExist:
        return None

    # Get the latest version
    dataset_version = DatasetVersion.objects\
            .select_related('dataset')\
            .filter(dataset=dataset,\
                versionstate=VERSION_STATE_RELEASED)\
            .order_by('-id').first()

    return dataset_version
