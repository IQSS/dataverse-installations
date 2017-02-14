"""
Given two dataset version in JSON format, find the differences
"""
import json
from os.path import join, isfile
from collections import OrderedDict
from dv_apps.utils.msg_util import msg, msgt, dashes


class DiffDescription(object):
    """Description of a single difference between Datasets"""

    def __init__(self, section, note, attr_name, new_val, old_val):
        """Minimal needed: section and note
        Other attributes:
            attr_name
            old_val
            new_val
        """
        self.section = section
        self.note = note
        self.attr_name = attr_name
        self.new_val = new_val
        self.old_val = old_val

    def show(self, show_section=True):
        """print info"""

        if show_section:
            msgt('%s: [%s] %s' % (self.section, self.attr_name, self.note))

        msg('attribute: %s' % self.attr_name)
        msg('\nnew: %s' % self.new_val)
        msg('\nold: %s' % self.old_val)
        dashes()


class DatasetDifferences(object):
    """Find differences between two datasets in JSON format"""

    def __init__(self, new_ds, old_ds):
        self.new_ds = new_ds
        self.old_ds = old_ds

        self.diff_found = False
        self.diff_list = []

    def add_diff(self, diff_dict):
        """Add a DiffDescription object"""
        self.diff_found = True

        self.diff_list.append(diff_dict)


    def get_diffferences(self):
        """If differences were found,
        return a list of DiffDescription objects"""

        if self.diff_found is False:
            return None

        return self.diff_list

    def run_comparison(self):
        """Compare the two JSON datasets"""
        msgt(self.run_comparison.__doc__)

        # Run a quick check to see if the dicts are the same.
        #
        if cmp(self.old_ds, self.new_ds) == 0:
            msg('No differences!')
            return

        new_files_list = self.new_ds.pop('files', [])
        old_files_list = self.old_ds.pop('files', [])
        #print 'new_files_list', new_files_list

        self.compare_dicts(\
                    '',
                    self.new_ds,
                    self.old_ds)

        self.compare_file_lists(\
                    new_files_list,
                    old_files_list)



    def compare_items(self, section, key_name, new_item, old_item, **kwargs):
        """Compare two items.  If they are dicts or lists, then
        compare each item in the dict or list"""


        # subsection used for dicts/lists
        if section:
            subsection = '%s : %s' % (section, key_name)
        else:
            subsection = key_name

        if isinstance(new_item, dict)\
            and isinstance(old_item, dict):
            # Yes, compare these dicts...
            #
            self.compare_dicts(subsection, new_item, old_item, **kwargs)

        elif isinstance(new_item, list) and isinstance(old_item, list):
            # Yes, compare these lists
            #
            self.compare_lists(subsection, new_item, old_item)

        else:
            # No, record the difference
            #
            self.record_diff_desc(\
                            section,
                            key_name,
                            new_item,
                            old_item)

    def get_array_label(self, cnt):
        """Used for labeling an item in a list
        e.g. "Item 1", "Item 2", etc"""
        return 'Item %s' % cnt


    def compare_file_lists(self, new_list, old_list):
        """Compare two lists of files

        TODO: Make sure comparing one file id to its equivalent
        """
        assert isinstance(new_list, list), 'new_list must be a list'
        assert isinstance(old_list, list), 'old_list must be a list'

        old_file_dict = dict([(file_info['id'], file_info)\
                             for file_info in old_list])

        section = 'Files'

        new_ids_used = []
        for new_item in new_list:
            print type(new_item)
            file_id = new_item.get('id')
            file_label = 'File %s' % file_id

            new_ids_used.append(file_id)

            # Does an older item exist with this file id?
            old_item = old_file_dict.get(file_id, None)

            if old_item:
                # Record items that have been CHANGED
                #
                if new_item != old_item:
                    self.compare_items(\
                                section,
                                file_label,
                                new_item,
                                old_item,
                                **dict(skip_list=['datasetVersionId']))
                del old_file_dict[file_id]  # remove from dict
            else:
                # Record items that have been ADDED
                #
                self.record_diff_desc_added(\
                            section,
                            file_label,
                            new_item)

        for file_id, old_item in old_file_dict.items():
            # Record items that have been REMOVED
            #
            file_label = 'File %s' % file_id

            self.record_diff_desc_removed(\
                            section,
                            file_label,
                            old_item)

    def compare_lists(self, section, new_list, old_list):
        """Compare two lists.  If an item in the list is another list
        or a dict, then compare each item in the dict or list"""

        assert isinstance(new_list, list), 'new_list must be a list'
        assert isinstance(old_list, list), 'old_list must be a list'

        cnt = 0
        for idx, new_item in enumerate(new_list):
            cnt = idx + 1

            if idx + 1 <= len(old_list):
                # Record items that have been CHANGED
                #
                old_item = old_list[idx]
                if new_item != old_item:
                    self.compare_items(\
                                section,
                                self.get_array_label(cnt),
                                new_item,
                                old_item)
            else:
                # Record items that have been ADDED
                #
                self.record_diff_desc_added(\
                            section,
                            self.get_array_label(cnt),
                            new_item)

        # Record items that have been REMOVED
        #
        if len(old_list) > len(new_list):
            for idx, old_item in enumerate(old_list[len(new_list):]):
                self.record_diff_desc_removed(\
                            section,
                            self.get_array_label(cnt),
                            old_item)

        #added = [new_item for new_item in set(new_list) if new_item not in old_list]
        #removed = [old_item for old_item in set(old_list) if old_item not in new_list]



    def record_diff_desc_removed(self, section, key, val):
        """This item was REMOVED from the newer version"""
        self.record_diff_desc(section, key, None, val)

    def record_diff_desc_added(self, section, key, val):
        """This item was ADDED from the newer version"""
        self.record_diff_desc(section, key, val, None)


    def record_diff_desc(self, section, key, new_val, old_val):
        """Make a DiffDescription object, noting whether
        a key/value was Removed, Added, or Modified"""

        if old_val and new_val is None:
            ds_diff = DiffDescription(\
                                section,
                                "Removed",
                                key,
                                self.format_for_display(None),
                                self.format_for_display(old_val))
        elif new_val and old_val is None:
            ds_diff = DiffDescription(\
                                section,
                                "Added",
                                key,
                                self.format_for_display(new_val),
                                self.format_for_display(None))
        else:
            ds_diff = DiffDescription(\
                                section,
                                "Modified",
                                key,
                                self.format_for_display(new_val),
                                self.format_for_display(old_val))
        self.add_diff(ds_diff)



    def format_for_display(self, item):

        if item is None:
            return '(blank)'

        elif isinstance(item, dict):
            fmt_lines = []
            for key, val in item.items():
                fmt_lines.append('<b>%s</b>: %s' % (key, self.format_for_display(val)))
            return '<br />'.join(fmt_lines)

        elif isinstance(item, list):
            #for val in item:
            return ','.join(item)

        return item


    def compare_dicts(self, section, new_dict, old_dict, **kwargs):
        """Compare two dicts, noting whether
        a key/value was Removed, Added, or Modified
        Note: Attempts to preserve key order--dict is usually an OrderedDict
        """
        # optional: get keys to skip
        skip_list = kwargs.get('skip_list', [])

        old_dict_keys = [key for key, val in old_dict.items()]
        new_dict_keys = [key for key, val in new_dict.items()]
        #old_dict_keys = set(old_dict.keys())
        #new_dict_keys = set(new_dict.keys())

        # ------------------------------
        # added attributes
        # ------------------------------
        added = [key for key in new_dict_keys if key not in old_dict_keys]
        #new_dict_keys - old_dict_keys
        for added_key in added:
            if added_key not in skip_list:
                self.record_diff_desc_added(\
                                section,
                                added_key,
                                new_dict[added_key])

        # ------------------------------
        # Removed attributes
        # ------------------------------
        removed = [key for key in old_dict_keys if key not in new_dict_keys]
        for removed_key in removed:
            if removed_key not in skip_list:
                self.record_diff_desc_removed(\
                                section,
                                removed_key,
                                old_dict[removed_key])

        # ------------------------------
        # Modified attributes
        # ------------------------------
        intersect_keys = [key for key in new_dict_keys\
                          if key not in removed and key not in added]
        mod_keys = [shared_key for shared_key in intersect_keys \
                    if old_dict[shared_key] != new_dict[shared_key]]

        for mod_key in mod_keys:
            msg('...> %s %s' % (mod_key, type(old_dict[mod_key])))
            # Is the value another dict?
            #
            if mod_key not in skip_list:
                self.compare_items(\
                            section,
                            mod_key,
                            new_dict[mod_key],
                            old_dict[mod_key])

    def show_diffs(self):
        """Debug: print out differences"""

        section = None
        for diff_obj in self.diff_list:
            if section != diff_obj.section:
                section = diff_obj.section
                msgt(section)
            diff_obj.show(show_section=False)
        #same = set(o for o in intersect_keys if old_dict[o] == new_dict[o])

        #return added, removed, modified, same


    @staticmethod
    def load_file_as_dict(fname):
        """Load a file as a python dict"""
        msgt('load file: %s' % fname)
        assert isfile(fname), '%s is not file' % fname

        fcontent = open(fname, 'r').read()
        fcontent = fcontent.replace('\r\n', '\\r\\n')

        dict_info = json.loads(fcontent, object_pairs_hook=OrderedDict)
        if dict_info.has_key('data'):
            return dict_info['data']

        return dict_info
