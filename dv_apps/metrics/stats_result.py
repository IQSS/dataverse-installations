import StringIO
import pandas as pd
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


    def was_succcess(self):
        if not self.error_found:
            return True
        return False

    def has_error(self):
        return self.error_found

    def add_error(self, err_msg):
        self.error_found = True
        self.error_message = err_msg

    def get_excel_workbook(self):
        """
        Convert data records to an excel notebook
        """
        if self.has_error():
            raise Exception("Error Found.  Call 'has_error()' before attempting this method.")

        assert self.result_data is not None, "result_data cannot be None"
        assert self.result_data.has_key('records'), "result_data must have a list of 'records'"

        records = self.result_data.get('records', None)
        assert records is not None, "records cannot be None"

        if len(records) == 0:
            return ''

        col_names = [ k for k, v in records[0].items()]

        excel_string_io = StringIO.StringIO()
        df = pd.DataFrame(self.result_data['records'])
        pd_writer = pd.ExcelWriter(excel_string_io, engine='xlsxwriter')

        df.to_excel(pd_writer, index=False, sheet_name='metrics', columns=col_names)
        pd_writer.save()

        excel_string_io.seek(0)
        workbook = excel_string_io.getvalue()

        return workbook


    def get_csv_content(self, as_excel=False):
        """
        Lots of assertions here.  We want to blow up for now--until test cases made
        or discovered
        """
        if self.has_error():
            raise Exception("Error Found.  Call 'has_error()' before attempting this method.")

        assert self.result_data is not None, "result_data cannot be None"
        assert self.result_data.has_key('records'), "result_data must have a list of 'records'"

        records = self.result_data.get('records', None)
        assert records is not None, "records cannot be None"

        if len(records) == 0:
            return ''

        col_names = [ k for k, v in records[0].items()]

        df = pd.DataFrame(self.result_data['records'])

        if as_excel:
            return df.to_excel(orient='records', index=False, columns=col_names)
        else:
            return df.to_csv(orient='records', index=False, columns=col_names)


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
