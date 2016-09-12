"""Convenience methods for getting total counts used on Dataverse.org"""

from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_files import StatsMakerFiles


def get_total_published_counts():
    """Get total counts for published dataverses, datasets, and files"""

    stats_dvs = StatsMakerDataverses()
    stats_ds = StatsMakerDatasets()
    stats_files = StatsMakerFiles()

    d = dict(total_dataverses=stats_dvs.get_dataverse_count_published().result_data,\
            total_datasets=stats_ds.get_dataset_count_published().result_data,
            total_files=stats_files.get_datafile_count_published().result_data,\
            total_downloads=stats_files.get_total_file_downloads().result_data,\
            )

    return d
