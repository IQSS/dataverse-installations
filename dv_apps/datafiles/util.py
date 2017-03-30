"""
Serialize a group of Datafiles based on the Dataset Version, similar to the native API:
    http://guides.dataverse.org/en/latest/api/native-api.html
"""
from collections import OrderedDict

from django.conf import settings
from django.db.models import F

from dv_apps.utils.date_helper import TIMESTAMP_MASK
from dv_apps.datafiles.models import Datafile, FileMetadata,\
    FilemetadataDatafileCategory, DatafileCategory
from dv_apps.datasets.models import DatasetVersion

class DatafileUtil(object):
    """Serialize a group of Datafile objects, similar to the Dataverse native API"""

    URL_FILE_ACCESS = '%s/api/access/datafile' % settings.DATAVERSE_INSTALLATION_URL

    KEY_ORDER1 = ['id',  'name', 'alias', 'dv_link',\
         'affiliation', 'dataversetype', 'description',\
         'publicationInfo',\
         'contacts', 'creator',\
         'ownerInfo', 'isRootDataverse',\
         'theme',\
         'metadatablockroot', 'templateroot',  'permissionroot',\
         'themeroot',  'facetroot', 'guestbookroot',\
         ]


    def __init__(self, dataset_version):
        assert isinstance(dataset_version, DatasetVersion), "You must pass a Dataverse object!"

        # set the DatasetVersion
        self.dsv = dataset_version

        # set the Dataset
        self.ds = dataset_version.dataset



    def as_json(self):
        """Serialize the Dataset Version"""

        # Retrieve the file metadata objects and related dvobjects
        #   Note: This is one of those weird (#@%~!) places where 'datafile'
        #       is an FK to the DvObject table and not to Datafile table
        f_metadata_objects = FileMetadata.objects.select_related('datafile'\
                                    ).filter(datasetversion=self.dsv\
                                    ).order_by('datafile__id')

        # filemetadata ids
        fmeta_ids = [x.id for x in f_metadata_objects]

        # Also the same as Datafile ids....
        dvobject_ids = [x.datafile.id for x in f_metadata_objects]

        # -----------------------------------------
        # Get dicts used for pulling data when
        # iterating through FileMetadata objects
        # -----------------------------------------
        dfiles = self.get_datafile_dict(dvobject_ids)
        #dcategories = self.get_datafile_categories(fmeta_ids)

        #print '-' * 40
        #print 'dcategories', dcategories
        #print '-' * 40

        fmeta_attrs = ('label', 'description', 'vers')
        fmt_list = []
        for fm in f_metadata_objects:
            od = OrderedDict()

            related_file = dfiles.get(fm.datafile.id)
            if related_file is None:
                raise Exception('related file not found for id: %s' % fm.datafile.id)

            # FileMetadata info
            od['id'] = related_file['id']
            od['datasetVersionId'] = self.dsv.id
            od['name'] = fm.label
            od['description'] = fm.description

            # --------------------------------
            # File info
            # --------------------------------
            file_info = OrderedDict()

            file_info['filesystemname'] = related_file['filesystemname']
            file_info['contentType'] = related_file['contenttype']
            file_info['filesize_bytes'] = related_file['filesize']

            # File checksum info
            checksum_info = OrderedDict()
            checksum_info['value'] = related_file['checksumvalue']
            checksum_info['type'] = related_file['checksumtype']

            file_info['checksum'] = checksum_info
            # --------------------------------

            od['specs'] = file_info

            od['restricted'] = related_file['restricted']
            od['ingeststatus'] = related_file['ingeststatus']
            od['file_access_url'] = '%s/%s' % (self.URL_FILE_ACCESS, related_file['id'])
            #DatafileUtil.get_file_access_url(datafile_id)
            od['timestamps'] = OrderedDict()
            od['timestamps']['createdate'] = fm.datafile.createdate.strftime(TIMESTAMP_MASK)
            if fm.datafile.publicationdate:
                od['timestamps']['publicationdate'] = fm.datafile.publicationdate.strftime(TIMESTAMP_MASK)
            else:
                od['timestamps']['publicationdate'] = None
            fmt_list.append(od)

        return fmt_list

    @staticmethod
    def get_file_access_url(datafile_id):
        """
        Return the Dataverse file access url
        example: http://localhost:8080/api/access/datafile/{ datafile_id }
        """
        return '%s/%s' % (DatafileUtil.URL_FILE_ACCESS, datafile_id)


    def get_datafile_categories(self, fmeta_ids):
        """
        fmeta_ids: FileMetadata ids
        """

        cat_ids = FilemetadataDatafileCategory.objects.filter(\
                    filemetadatas__in=fmeta_ids\
                    ).values_list('filemetadatas__id', flat=True)

        l = DatafileCategory.objects.select_related('filecategories'\
                ).filter(filemetadatas__in=fmeta_ids\
                ).annotate(fmeta_id=F('filemetadatas__id'),\
                    category=F('filecategories__name')
                ).values('fmeta_id', 'category')

        print l.query
        # create dict of { fmeta_id : [category, category, etc], }
        #
        d = {}  # { fmeta_id : [category, category, etc], }
        for info in l:
            d.setdefault(info.fmeta_id, []).append(info.category)

        return d


    def get_datafile_dict(self, dvobject_ids):
        """
        Retrieve Datafile objects and return as a dict with key being the id
        """
        vals = ('id', 'contenttype', 'filesystemname',\
            'filesize', 'checksumtype', 'checksumvalue', 'restricted',\
            'ingeststatus')
        dfiles = Datafile.objects.filter(dvobject__id__in=dvobject_ids\
            ).annotate(id=F('dvobject__id')\
            ).values(*vals)

        d = {}
        for dinfo in dfiles:
            d[dinfo['id']] = dinfo

        return d

'''
    {
      "description": "",
      "label": "year1972.data",
      "version": 1,
      "datasetVersionId": 119,
      "datafile": {
        "id": 2514306,
        "name": "year1972.data",
        "contentType": "application/octet-stream",
        "filename": "http://irss-arc1/dvn/dv/NCVITAL/FileDownload/year1972.data?fileId=3160039",
        "originalFormatLabel": "UNKNOWN",
        "md5": "",
        "description": ""
      }
    },
'''

'''
import requests

fid = 2668709
URL_FILE_ACCESS = 'https://dataverse.harvard.edu/api/access/datafile/%s' % fid

r = requests.get('https://api.github.com/events', stream=True)

fname = 'some.xlsx'
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
'''
