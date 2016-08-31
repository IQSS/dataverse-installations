"""
Holds the results of metrics queries from:
    StatsMakerDataverses
    StatsMakerDatasets
    StatsMakerFiles
"""
class StatsResult(object):

    def __init__(self, **kwargs):
        """Object to hold results from a stats query"""
        self.error_found = kwargs.get('error_found', False)
        self.error_message = kwargs.get('error_message', False)
        self.bad_http_status_code = kwargs.get('bad_http_status_code', None)

        self.result_data = kwargs.get('result_data', None)
        if self.result_data:
            self.error_found = False
        self.sql_query = kwargs.get('sql_query', None)

        # Used downstream for CSVs
        self.as_csv = False
        self.csv_header_keys = None

    def was_succcess(self):
        if not self.error_found:
            return True
        return False

    def has_error(self):
        return self.error_found

    @staticmethod
    def build_error_result(error_message, bad_http_status_code=None):
        """
        Return an error result with an error message
        and optional http status code
        """
        d = dict(error_found=True,\
                error_message=error_message,\
                bad_http_status_code=bad_http_status_code)
        sr = StatsResult(**d)
        return sr

    @staticmethod
    def build_success_result(metrics_records, sql_query=None):
        """
        Return a successful result with data and
        optioanl sql query string
        """
        #import ipdb; ipdb.set_trace()
        d = { 'result_data' : metrics_records,\
                'sql_query' : sql_query}
        sr = StatsResult(**d)
        return sr
