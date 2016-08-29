"""
Serialize a group of Datafiles based on the Dataset Version, similar to the native API:
    http://guides.dataverse.org/en/latest/api/native-api.html
"""
from collections import OrderedDict

from django.conf import settings
from django.db.models import F

from dv_apps.utils.date_helper import TIMESTAMP_MASK
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.datasets.models import DatasetVersion

class DatafileUtil(object):
    """Serialize a group of Datafile objects, similar to the Dataverse native API"""

    URL_BASE = '%s/file' % settings.DATAVERSE_INSTALLATION_URL

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
        f_metadata_objects = FileMetadata.objects.select_related('datafile').filter(datasetversion=self.dsv)

        # Also the same as Datafile ids....
        dvobject_ids = [x.datafile.id for x in f_metadata_objects]

        dfiles = self.get_datafile_dict(dvobject_ids)
        print '-' * 40
        print 'dfiles', dfiles
        print '-' * 40

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

            file_info = OrderedDict()

            file_info['filesystemname'] = related_file['filesystemname']
            file_info['contentType'] = related_file['contenttype']
            file_info['filesize_bytes'] = related_file['filesize']
            file_info['md5'] = related_file['md5']
            od['specs'] = file_info

            od['restricted'] = related_file['restricted']
            od['ingeststatus'] = related_file['ingeststatus']
            od['download_url'] = 'oh my my'

            od['timestamps'] = OrderedDict()
            od['timestamps']['createdate'] = fm.datafile.createdate.strftime(TIMESTAMP_MASK)
            if fm.datafile.publicationdate:
                od['timestamps']['publicationdate'] = fm.datafile.publicationdate.strftime(TIMESTAMP_MASK)
            else:
                od['timestamps']['publicationdate'] = None
            fmt_list.append(od)

        return fmt_list

    def get_datafile_dict(self, dvobject_ids):
        """
        Retrieve Datafile objects and return as a dict with key being the id
        """
        vals = ('id', 'contenttype', 'filesystemname',\
            'filesize', 'md5', 'restricted',\
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
