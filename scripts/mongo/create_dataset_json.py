import os, sys
from os.path import dirname, isdir, isfile, join, realpath

#-------------------------------------------
# start: Django setup
#-------------------------------------------
SCRIPT_DIR = dirname(realpath(__file__))
PROJ_PATH = dirname(dirname(SCRIPT_DIR))
sys.path.append(PROJ_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniverse.settings.local_with_routing")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#-------------------------------------------
# end: Django setup
#-------------------------------------------
from pymongo import MongoClient

import json
from datetime import datetime
import time
from collections import OrderedDict

from django.utils.text import slugify
from django.db.models import F

from dv_apps.datasets.models import Dataset
from dv_apps.datasets.serializer import DatasetSerializer
from dv_apps.datasets.util import get_latest_dataset_version
from dv_apps.utils.msg_util import msg, msgt, msgx
from mongo_rename_list import update_json_text

OUTPUT_DIR = join(SCRIPT_DIR, 'json_output')
if not isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class DatasetJSONCreator(object):

    def __init__(self, **kwargs):

        self.dataset_start_id = kwargs.get('dataset_start_id', 0)
        self.overwrite_existing_files = kwargs.get('overwrite_existing_files', False)
        self.output_dir = kwargs.get('output_dir', OUTPUT_DIR)
        self.published_only = kwargs.get('published_only', True)
        assert isdir(self.output_dir),\
            "Output directory does not exist: %s" % self.output_dir

    def make_json_files(self):

        # Set publication status
        #
        filters = {}
        if self.published_only:
            filters.update(dict(dvobject__publicationdate__isnull=False))

        # Query for dataset ids
        #
        ds_id_query = Dataset.objects.filter(**filters\
                            ).annotate(ds_id=F('dvobject__id')\
                            ).values_list('ds_id', flat=True\
                            ).order_by('ds_id')

        # Iterate through dataset ids
        #
        #start_time = datetime.now()
        start_time = int(time.time()) # epoch seconds

        cnt = 0
        no_versions_found_list = [45900]

        for ds_id in ds_id_query:
            cnt += 1
            msgt('(%d) Checking dataset id %s' % (cnt, ds_id))
            if ds_id < self.dataset_start_id:
                msg('skipping...(start at dataset id: %d)' % self.dataset_start_id)
                continue

            # Create file name
            #
            fname = 'ds_%s.json' % (str(ds_id).zfill(8))
            full_fname = join(OUTPUT_DIR, fname)

            # Should we overwrite the existing file?
            #
            if isfile(full_fname) and not self.overwrite_existing_files:
                msg('skipping...file already exists')
                continue

            dataset_version = get_latest_dataset_version(ds_id)

            if dataset_version is None:
                msg("Could not find dataset_version!")
                no_versions_found_list.append(ds_id)
                continue

            dataset_as_json = DatasetSerializer(dataset_version).as_json()

            open(full_fname, 'w').write(json.dumps(dataset_as_json, indent=4))
            msg('File written: %s' % full_fname)

            if cnt % 500 == 0:
                self.show_elapsed_time(start_time)
            #if cnt > 10:
            #    self.show_elapsed_time(start_time)
            #    break

        self.show_elapsed_time(start_time)
        print 'no_versions_found_list: %s' % no_versions_found_list

    def show_elapsed_time(self, start_time):
        """From http://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python"""
        time_now = int(time.time()) # epoch seconds

        days = divmod(time_now - start_time, 86400)  # days

        hours = divmod(days[1], 3600)  # hours
        minutes = divmod(hours[1],60)  # minutes
        seconds = minutes[1]  # seconds

        msgt('Elapsed time: %d day(s), %d hour(s), %d minute(s), %d second(s)' % (days[0],hours[0],minutes[0],seconds))

    def write_files_to_mongo(self, **kwargs):
        """Write the saved dataset files to Mongo"""
        client = MongoClient()
        db = client.dataverse_database
        collection = db.datasets

        # look at kwargs
        #
        dataset_start_id = kwargs.get('dataset_start_id', 0)
        delete_all = kwargs.get('delete_all', False)

        # If appropriate, Delete existing records
        #
        if delete_all:
            msgt('Deleting current records')
            result = collection.delete_many({})
            msg('result.deleted_count: %s' %  result.deleted_count)
            return

        fnames = os.listdir(self.output_dir)
        fnames = [x for x in fnames if x.endswith('.json') and x.startswith('ds_')]
        fnames.sort()

        start_time = int(time.time()) # epoch seconds

        cnt = 0
        for fname in fnames:
            cnt += 1
            ds_id = int(fname.split('.')[0].split('_')[1])

            msgt('(%d) process dataset %s (%s)' % (cnt, ds_id, fname))

            if ds_id < dataset_start_id:
                msg('skipping it')
                continue

            content = open(join(self.output_dir, fname), 'r').read()
            content = update_json_text(content)
            content_doc = json.loads(content, object_pairs_hook=OrderedDict)
            content_doc['_id'] = ds_id
            content_doc['dtype'] = 'dataset'

            #doc_id = collection.insert_one(content_doc).inserted_id
            #doc_id = collection.save(content_doc)   #.inserted_id
            doc_id = collection.save(content_doc)
            if cnt % 500 == 0:
                self.show_elapsed_time(start_time)
        self.show_elapsed_time(start_time)


    def test_search_mongo(self, term='law'):
        """Test searches"""
        client = MongoClient()
        db = client.dataverse_database
        collection = db.datasets

        # Compass:
        #
        # {"title": {$regex: "(^Law| Law | Law$)"}}
        """
        {"title":{"$regex":"(^Law| Law | Law$)","$options":"i"},"metadata_blocks.citation.dsDescription.dsDescriptionValue": {"$regex":"(^Law| Law | Law$)","$options":"i"}}
        """
        field_names = [
                    'metadata_blocks.citation.dsDescription.dsDescriptionValue',
                    #'title',
                    #'metadata_blocks.citation.subject',                 #'metadata_blocks.citation.keyword.keywordValue',
                    ]

        qlist = []
        for field_name in field_names:
            qlist.append({ field_name: {'$regex':'(^{0}|\s{0}\s|\s{0}$)'.format(term),
                                        '$options':'i'}}
                        )
        docs = collection.find({"$or": qlist})


        # -----------------------------
        #field_name = 'title'
        #field_name = 'metadata_blocks.citation.dsDescription.dsDescriptionValue'
        #docs = collection.find({field_name:{'$regex':'(^Law|\sLaw\s|\sLaw$)', '$options':'i'}})
        #docs = collection.find({'title':{'$regex':'(^Law|\sLaw\s|\sLaw$)', '$options':'i'}})
        from dict_map_util import DictMapUtil

        cnt = 0
        for doc in docs:
            cnt += 1
            msgt('(%d) %s' % (cnt, doc['title']))

            dmap_str = 'dmap.' + field_names[0]
            print 'dmap_str', dmap_str
            m = DictMapUtil(doc)
            import ipdb; ipdb.set_trace()
            #print eval(dmap_str)
            break
            """
            keys = field_names[0].split('.')
            new_doc = doc
            for key in keys:
                #print key, keys
                if new_doc is dict:
                    new_doc = new_doc.get(key, {})
                elif new_doc is list:
                    for item in new_doc:
                        if item.has_key('key'):
                            new_doc = item.get('key')
            print 'match: %s' % new_doc
            """

if __name__ == '__main__':
    start_kwargs = dict(dataset_start_id=0,
                    overwrite_existing_files=False)

    json_creator = DatasetJSONCreator(**start_kwargs)

    # (1) Make the JSON files
    #json_creator.make_json_files()

    # (2) Write the JSON files to Mongo
    #
    #mongo_kwargs = dict(delete_all=False,\
    #                    dataset_start_id=0)
    #json_creator.write_files_to_mongo(**mongo_kwargs)

    # (3) Test search Mongo
    #
    json_creator.test_search_mongo()
