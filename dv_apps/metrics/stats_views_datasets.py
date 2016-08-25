from dv_apps.metrics.stats_view_base import StatsViewSwagger
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
# limit the API rates
#from ratelimit.decorators import ratelimit



class DatasetTotalCounts(StatsViewSwagger):
    """API View - Total count of all Dataverses"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/count'
    summary = ('Simple count of published Datasets')
    description = ('Returns number of published Datasets')
    description_200 = 'Number of published Datasets'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY + StatsViewSwagger.PUBLISH_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM
    tags = [StatsViewSwagger.TAG_DATASETS]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasets(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataset_count()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataset_count_unpublished()
        else:
            stats_result = stats_datasets.get_dataset_count_published()

        return stats_result


class DatasetCountByMonthView(StatsViewSwagger):
    """API View - Published Dataset counts by Month"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/count/monthly'
    summary = ('Number of published Datasets by'
            ' the month they were created*.  (*'
            ' Not month published)')
    description = ('Returns a list of counts and'
            ' cumulative counts of all datasts added in a month')
    description_200 = 'A list of Dataset counts by month'
    tags = [StatsViewSwagger.TAG_DATASETS]


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasets(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataset_counts_by_create_date()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataset_counts_by_create_date_unpublished()
        else:
            stats_result = stats_datasets.get_dataset_counts_by_create_date_published()

        return stats_result



class DatasetSubjectCounts(StatsViewSwagger):
    """API View - Number of Datasets by Subject"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/datasets/count/by-subject'
    summary = ('Number of Datasets by Subject')
    description = ('Number of Datasets by Subject')
    description_200 = ('Number of Datasets by Subject')
    tags = [StatsViewSwagger.TAG_DATASETS]
    result_name = StatsViewSwagger.RESULT_NAME_DATASET_SUBJECT_COUNTS


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasets(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataset_subject_counts()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataset_subject_counts_unpublished()
        else:
            stats_result = stats_datasets.get_dataset_subject_counts_published()

        return stats_result
