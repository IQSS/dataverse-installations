from os.path import basename, isfile, getsize
from collections import OrderedDict
import json
import pandas as pd

from dv_apps.utils.msg_util import msgt, msg
from dv_apps.datafiles import temp_file_helper

DEFAULT_PREVIEW_ROW_LIMIT = 50

class TabularPreviewer(object):
    """Preview first x rows of a Tabular File
    Used to produce JSON for widgets"""

    def __init__(self, filepath, **kwargs):

        # set params from kwargs or default
        self.num_preview_rows = kwargs.get('num_preview_rows', DEFAULT_PREVIEW_ROW_LIMIT)
        self.tab_delimiter = kwargs.get('tab_delimiter', '\t')

        self.is_excel = False#kwargs.get('is_excel', False)

        # summary info
        self.describe_as_dict = None
        self.describe_as_html = None
        self.column_names = None
        self.data_rows = None

        # filepath
        self.filepath = filepath
        self.file_ext = kwargs.get('file_ext', None)

        # internal error check
        self.error_found = False
        self.error_message = None


        self.preliminary_file_check()


    def add_error(self, err_msg):
        """Add an error message"""
        assert err_msg is not None, 'err_msg cannot be None'

        self.error_found = True
        self.error_message = err_msg.strip()

    def has_error(self):
        """Did an error occur?"""
        return self.error_found

    def preliminary_file_check(self):
        """Make sure the file exists and isn't empty"""

        if self.has_error():
            return False

        if not self.filepath:
            self.add_error("A file was specified!")
            return False

        if not isfile(self.filepath):
            self.add_error("The file was not found: %s" % basename(self.filepath))
            return False

        if getsize(self.filepath) < 1:
            self.add_error("The file is empty (no bytes): %s" % basename(self.filepath))
            return False

        if self.file_ext in ['xls', 'xlsx']:
            self.is_excel = True

        return True

    def get_json_rows(self, pretty_print=False):
        return self.get_data_rows(as_json=True, pretty_print=pretty_print)

    def get_data_rows(self, as_json=False, pretty_print=False):
        """
        Return information as JSON
            {
                "data" :
                    "total_row_count" : 117
                    "preview_row_count" : 50
                    "column_names" : ["Name", "Position", "Office"]
                    "rows" : [
                        [
                          "Tiger Nixon",
                          "System Architect",
                          "Edinburgh"
                        ],
                        [
                          "Garrett Winters",
                          "Accountant",
                          "Tokyo"
                        ]
                    ]
            }
        """
        if self.has_error():
            return None

        # Read the table
        try:
            if self.is_excel:
                msgt('Excel!')
                df = pd.read_table(self.filepath,
                                   error_bad_lines=False)
            else:
                df = pd.read_table(self.filepath)
        except Exception as ex_obj:
            msg(ex_obj)
            msgt('Failed to open file via pandas!')
            temp_file_helper.make_sure_file_deleted(self.filepath)
            if self.is_excel:
                self.add_error('Failed to open Excel file via pandas. [%s]' % ex_obj)
            else:
                self.add_error('Failed to open file via pandas. [%s]' % ex_obj)
            return None

        self.describe_as_html = df.describe().to_html()
        json_string = df.describe().to_json()
        self.describe_as_dict =json.loads(json_string, object_pairs_hook=OrderedDict)

        # Retrieve the columns
        self.column_names = df.columns.tolist()

        # Retrieve the rows
        self.data_rows = df[:self.num_preview_rows].values.tolist()

        #print 'rows', json.dumps(rows)

        # Format the response
        info_dict = OrderedDict()

        info_dict['total_row_count'] = len(df.index)
        info_dict['preview_row_count'] = len(self.data_rows)
        info_dict['column_names'] = self.column_names
        info_dict['rows'] = self.data_rows
        info_dict['describe_as_html'] = self.describe_as_html
        info_dict['describe_as_dict'] = self.describe_as_dict

        if as_json:
            if pretty_print:
                return json.dumps(info_dict, indent=4)
            return json.dumps(info_dict)

        return info_dict
