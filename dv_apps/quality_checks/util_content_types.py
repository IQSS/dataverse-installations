"""
Check for files without content types--or "unknown" content type
"""
from dv_apps.metrics.stats_util_files import StatsMakerFiles, FILE_TYPE_OCTET_STREAM
from dv_apps.quality_checks.named_stat import NamedStat

class ContentTypeStats(object):
    """Check for files without content types--or "unknown" content type"""
    def __init__(self):
        pass

    @staticmethod
    def get_basic_stats():

        stats_files = StatsMakerFiles()
        stats_result = stats_files.view_file_extensions_within_type(FILE_TYPE_OCTET_STREAM)
        if not (stats_result and stats_result.result_data):
            raise ValueError('ContentTypeStats not calculated for content types')

        print 'type(stats_result.result_data)', type(stats_result.result_data)
        print 'type(stats_result)', type(stats_result)
        print 'keys', stats_result.result_data.keys()

        records = stats_result.result_data.get('records')
        #print 'stats_result', stats_result
        total_file_count = stats_result.result_data.get('total_file_count')
        number_unique_extensions = stats_result.result_data.get('number_unique_extensions')
        all_dv_files_count = stats_result.result_data.get('all_dv_files')
        percent_unknown = stats_result.result_data.get('percent_unknown')


        file_stats = dict(\
            cnt_no_content_type=NamedStat(\
                'No Content Type',
                total_file_count,
                ('Counts of FileMetadata objects with an unknown content type'),
                'view_files_extensions_with_unknown_content_types'),
            percent_no_content_type=NamedStat(\
                '% No Content Type',
                percent_unknown,
                ('Percent of FileMetadata objects with an unknown content type'),
                'view_files_extensions_with_unknown_content_types'),
                )

        return file_stats
