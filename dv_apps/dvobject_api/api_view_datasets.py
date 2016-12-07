"""Dataset related API endpoints"""

from dv_apps.metrics.stats_view_base import StatsViewSwagger
from dv_apps.metrics.stats_result import StatsResult
from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.datasets.util import DatasetUtil


#from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
# limit the API rates
#from ratelimit.decorators import ratelimit

class DatasetByIdView(StatsViewSwagger):
    """View a Dataset By Id"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/by-id/{ds_id}'
    summary = ('Retrieve published Dataset object in JSON format.')
    description = ('Retrieve published Dataset object in JSON format.')
    description_200 = 'Retrieve published Dataset object in JSON format.'
    param_names = StatsViewSwagger.PARAM_DATASET_ID\
                + StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                #+ StatsViewSwagger.PUBLISH_PARAMS
    #tags = [StatsViewSwagger.TAG_TEST_API]
    tags = [StatsViewSwagger.TAG_TEST_API]
    result_name = StatsViewSwagger.RESULT_NAME_DATASET

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""

        dv_id = self.kwargs.get('ds_id', None)
        if dv_id is None:
            return StatsResult.build_error_result("No Dataset id specified", 400)

        # Get the latest version
        dataset_version = get_latest_dataset_version(dv_id)

        if dataset_version is None:
            return StatsResult.build_error_result('No published Dataset with id: %s' % dv_id, 404)

        dataset_as_json = DatasetUtil(dataset_version).as_json()

        return StatsResult.build_success_result(dataset_as_json)


class DatasetByPersistentIdView(StatsViewSwagger):
    """View a Dataset By Id"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/by-persistent-id'
    summary = ('Retrieve published Dataset object in JSON format.')
    description = ('Retrieve published Dataset object in JSON format.')
    description_200 = 'Retrieve published Dataset object in JSON format.'
    param_names = StatsViewSwagger.PARAM_DATASET_PERSISTENT_ID\
                + StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                #+ StatsViewSwagger.PUBLISH_PARAMS
    #tags = [StatsViewSwagger.TAG_TEST_API]
    tags = [StatsViewSwagger.TAG_TEST_API]
    result_name = StatsViewSwagger.RESULT_NAME_DATASET

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        persistent_id = request.GET.get('persistentID', None)
        if persistent_id is None:
            return StatsResult.build_error_result("No Dataset persistent id specified", 400)

        ds = Dataset.get_dataset_by_persistent_id(persistent_id)

        err_404 = 'No published dataset found for persistentID: %s' % persistent_id

        if ds is None or not ds.dvobject.publicationdate:
            return StatsResult.build_error_result(err_404, 404)


        # Get the latest version
        dataset_version = get_latest_dataset_version(ds.dvobject.id)

        if dataset_version is None:
            return StatsResult.build_error_result(err_404, 404)

        dataset_as_json = DatasetUtil(dataset_version).as_json()

        return StatsResult.build_success_result(dataset_as_json)


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
