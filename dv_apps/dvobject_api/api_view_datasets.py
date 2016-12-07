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
    api_path = '/datasets/by-id/{dv_id}'
    summary = ('Retrieve published Dataset object in JSON format.')
    description = ('Retrieve published Dataset object in JSON format.')
    description_200 = 'Retrieve published Dataset object in JSON format.'
    param_names = StatsViewSwagger.PARAM_DVOBJECT_ID\
                + StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                #+ StatsViewSwagger.PUBLISH_PARAMS
    #tags = [StatsViewSwagger.TAG_TEST_API]
    tags = [StatsViewSwagger.TAG_TEST_API]
    result_name = StatsViewSwagger.RESULT_NAME_DATASET

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""

        dv_id = self.kwargs.get('dv_id', None)
        if dv_id is None:
            return StatsResult.build_error_result("No Dataset id specified", 400)

        try:
            dataset = Dataset.objects.select_related('dvobject').get(\
                dvobject__id=dv_id,\
                dvobject__publicationdate__isnull=False)
        except Dataset.DoesNotExist:
            return StatsResult.build_error_result('No published Dataset with id: %s' % dv_id, 404)

        # Get the latest version
        dataset_version = DatasetVersion.objects\
                .select_related('dataset')\
                .filter(dataset=dataset,\
                    versionstate=VERSION_STATE_RELEASED)\
                .order_by('-id').first()

        if dataset_version is None:
            return StatsResult.build_error_result('No published Dataset with id: %s' % dv_id, 404)

        dataset_as_json = DatasetUtil(dataset_version).as_json()

        return StatsResult.build_success_result(dataset_as_json)
