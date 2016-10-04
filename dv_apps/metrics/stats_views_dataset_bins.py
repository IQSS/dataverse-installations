from dv_apps.metrics.stats_view_base import StatsViewSwagger
from dv_apps.metrics.stats_util_datasets_bins import StatsMakerDatasetBins
# limit the API rates
#from ratelimit.decorators import ratelimit



class FilesPerDatasetStats(StatsViewSwagger):
    """API View - Counts of Files Per Dataset Using the Latest DatasetVersion"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/file-stats'
    summary = ('Counts of files per Dataset using the latest DatasetVersion')
    description = ('Counts of files per Dataset using the latest DatasetVersion')
    description_200 = 'Counts of files per Dataset using the latest DatasetVersion'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PUBLISH_PARAMS\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                + StatsViewSwagger.PARAM_BIN_SIZE\
                + StatsViewSwagger.PARAM_SKIP_EMPTY_BINS\
                + StatsViewSwagger.PARAM_AS_CSV
                #+ StatsViewSwagger.PARAM_NUM_BINS\

    tags = [StatsViewSwagger.TAG_DATASETS]
    result_name = StatsViewSwagger.RESULT_NAME_BIN_COUNTS

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasetBins(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_file_counts_per_dataset_latest_versions()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_file_counts_per_dataset_latest_versions_unpublished()
        else:
            stats_result = stats_datasets.get_file_counts_per_dataset_latest_versions_published()

        return stats_result
