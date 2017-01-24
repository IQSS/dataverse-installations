from os.path import basename, isfile, getsize
from collections import OrderedDict
import json
import pandas as pd

from dv_apps.datafiles import temp_file_helper

DEFAULT_PREVIEW_ROW_LIMIT = 50

class TabularPreviewer(object):
    """Preview first x rows of a Tabular File
    Used to produce JSON for widgets"""

    def __init__(self, filepath, **kwargs):

        # set params from kwargs or default
        self.num_preview_rows = kwargs.get('num_preview_rows', DEFAULT_PREVIEW_ROW_LIMIT)
        self.tab_delimiter = kwargs.get('tab_delimiter', '\t')

        # filepath
        self.filepath = filepath

        # internal error check
        self.error_found = False
        self.error_message = None

        self.preliminary_file_check()

    def add_error(self, err_msg):
        """Add an error message"""
        self.error_found = True
        self.error_message = err_msg

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
            df = pd.read_table(self.filepath)
        except:
            msgt('Failed to open file via pandas!')
            temp_file_helper.make_sure_file_deleted(self.filepath)
            return None

        # Retrieve the columns
        column_names = df.columns.tolist()

        # Retrieve the rows
        rows = df[:self.num_preview_rows].values.tolist()

        #print 'rows', json.dumps(rows)

        # Format the response
        info_dict = OrderedDict()

        info_dict['total_row_count'] = len(df.index)
        info_dict['preview_row_count'] = len(rows)
        info_dict['column_names'] = column_names
        info_dict['rows'] = rows

        if as_json:
            if pretty_print:
                return json.dumps(info_dict, indent=4)
            return json.dumps(info_dict)

        return info_dict
