from dv_apps.metrics.stats_view_base import StatsViewSwagger, StatsViewSwaggerKeyRequired
from dv_apps.metrics.stats_util_datasets_bins import StatsMakerDatasetBins
from dv_apps.metrics.stats_util_dataset_size import StatsMakerDatasetSizes
# limit the API rates
#from ratelimit.decorators import ratelimit



class FilesPerDatasetStats(StatsViewSwaggerKeyRequired):
    """API View - Counts of Files Per Dataset Using the Latest DatasetVersion"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/file-stats'
    summary = ('Counts of files per Dataset using the latest DatasetVersion')
    description = ('Counts of files per Dataset using the latest DatasetVersion.'
                ' Answers the question -> How many datasets have "x" number of'
                ' files?  For example, if the "bin_size" is set to 20, results will show'
                ' the number of datasets with 0 to 19 files, the number of datasets with'
                ' 20 to 29 files, etc.')
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



class BytesPerDatasetStats(StatsViewSwaggerKeyRequired):
    """API View - Answers the question: How many datasets have "x" number of bytes?"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/bytes-used'
    summary = ('Counts of published datasets based on total bytes of storage used')
    description = ('Counts of datasets based on total bytes of storage used.'
                ' Answers the question -> How many datasets have "x" number of bytes?'
                ' For example, if the "bin_size" is set to 52428800, results will show'
                ' the number of datasets with "0.0 B to 50.0 MB" of data, the number of datasets with'
                ' "50.0 MB to 100.0 MB", etc.')
    description_200 = 'Counts of files per Dataset using the latest DatasetVersion'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY\
                + StatsViewSwagger.PUBLISH_PARAMS\
                + StatsViewSwagger.PRETTY_JSON_PARAM\
                + StatsViewSwagger.PARAM_BIN_SIZE_BYTES\
                + StatsViewSwagger.PARAM_SKIP_EMPTY_BINS\
                + StatsViewSwagger.PARAM_AS_CSV

    tags = [StatsViewSwagger.TAG_DATASETS]
    result_name = StatsViewSwagger.RESULT_NAME_BIN_COUNTS_SIZES


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasetSizes(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataset_size_counts()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataset_size_counts_unpublished()
        else:
            stats_result = stats_datasets.get_dataset_size_counts_published()

        return stats_result
