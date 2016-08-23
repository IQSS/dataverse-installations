"""
Serialize a Dataset object, similar to the native API:
    http://guides.dataverse.org/en/latest/api/native-api.html

Note: creator may be inaccurate.  These models assume it's an AuthenticatedUser
    - When is it not?  (e.g. group creates a Dataverse)
"""
from collections import OrderedDict

from django.forms.models import model_to_dict

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datasetfields.utils import get_dataset_title
from dv_apps.datasetfields.metadata_formatter import MetadataFormatter



class DatasetUtil(object):
    """Serialize a Dataset object, similar to the Dataverse native API"""

    # Hack URL - NEEDs to be based on installation
    URL_BASE = 'https://dataverse.harvard.edu/dataset.xhtml?persistentId='

    TIMESTAMP_MASK = '%Y-%m-%d %H:%M:%S'
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

        # set the DvObject
        self.dvobject = dataset_version.dataset.dvobject


    def as_json(self):
        """Serialize the Dataset Version"""

        # Get the title
        #
        success, dataset_title_or_err = get_dataset_title(self.dsv)
        if not success:
            return False, \
                dict(error_message='Could not find Dataset title. %s' % dataset_title_or_err)

        # -----------------------------------
        # Hold the Dataset info, starting with title
        # -----------------------------------
        dsv_metadata = OrderedDict()
        dsv_metadata['title'] = dataset_title_or_err
        dsv_metadata['id'] = self.dvobject.id

        # doi/handle
        #
        persistent_id_info = OrderedDict()
        persistent_id_info['protocol'] = self.ds.protocol
        persistent_id_info['authority'] = self.ds.authority
        persistent_id_info['identifier'] = self.ds.identifier
        persistent_id_info['persistentId'] = self.ds.identifier_string()

        dsv_metadata['persistentIdInfo'] = persistent_id_info

        # semanticVersionInfo
        #
        semantic_version_info = OrderedDict()
        semantic_version_info['semantic_version'] = self.dsv.get_semantic_version()
        semantic_version_info['versionNumber'] = self.dsv.versionnumber
        semantic_version_info['versionMinorNumber'] = self.dsv.minorversionnumber
        semantic_version_info['versionState'] = self.dsv.versionstate
        dsv_metadata['semanticVersionInfo'] = semantic_version_info

        dsv_metadata['dv_link'] = self.get_dv_link(semantic_version_info['semantic_version'])



        # -----------------------------------
        # Format the metadata blocks -- the heavy lift...
        # -----------------------------------
        mdf = MetadataFormatter(self.dsv)
        dsv_metadata['metadata_blocks'] = mdf.as_dict().get('metadata_blocks',{})

        return dsv_metadata

    def get_dv_link(self, semantic_version):
        """
        Format a link to this Dataverse.
        - Scratch work.  Need to get URL_BASE from settings or sites framework
        """
        if semantic_version:
            return '%s%s&?version=%s' % (self.URL_BASE,\
                self.ds.identifier_string(),\
                semantic_version)
        else:
            return '%s/%s' % (self.URL_BASE,\
                self.ds.identifier_string())

"""
{
  "status": "OK",
  "data": {
    "id": 4119,
    "identifier": "10216",
    "persistentUrl": "http://hdl.handle.net/1902.29/10216",
    "protocol": "hdl",
    "authority": "1902.29",
    "latestVersion": {
      "id": 119,
      "versionNumber": 1,
      "versionMinorNumber": 0,
      "versionState": "RELEASED",
      "versionNote": "Initial version",
      "productionDate": "Production Date",
      "lastUpdateTime": "2014-12-13T06:53:29Z",
      "releaseTime": "2008-10-01T00:00:00Z",
      "createTime": "2008-11-01T05:11:40Z",
      "metadataBlocks": {
        "citation": {
          "displayName": "Citation Metadata",
          "fields": [
            {
              "typeName": "title",
              "multiple": false,
              "typeClass": "primitive",
              "value": "North Carolina Vital Statistics -- Birth/Infant Deaths 1972"
            },
            {
              "typeName": "author",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "authorName": {
                    "typeName": "authorName",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "State Center for Health Statistics"
                  }
                }
              ]
            },
            {
              "typeName": "datasetContact",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "datasetContactName": {
                    "typeName": "datasetContactName",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "David Sheaves"
                  },
                  "datasetContactEmail": {
                    "typeName": "datasetContactEmail",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "david_sheaves@unc.edu"
                  }
                }
              ]
            },
            {
              "typeName": "dsDescription",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "dsDescriptionValue": {
                    "typeName": "dsDescriptionValue",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "<p>The North Carolina State Center for Health Services (SCHS) collects yearly vital statistics. The Odum Institute holds vital statistics beginning in 1968 for births, fetal deaths, deaths, birth/infant deaths, marriages and divorce. Public marriage and divorce data are available through 1999 only.</p><p>We have created a consolidated birth/infant death file that contains records of deaths occurring during the first year of life. Each such death record has been matched with a corresponding birth\nrecord creating a composite record containing information about both events. Users of these consolidated files should be aware that the file year of these data sets refers to the year of birth, not the year of death. For example, the 1970 consolidated birth/infant death file contains records of births occurring during 1970 that ended in an infant death either in 1970 or 1971. For this reason, the number of infant deaths for a particular year as obtained from the consolidated file will not be the same as the number obtained\nfrom the death file for that same year. This difference should especially be kept in mind when using this file in conjunction with the publication Vital Statistics, volume 1. This study focuses on North Carolina birth/infant deaths for 1972. It includes data on the age, education level and marital status of the parents; sex and race of the child; prenatal medical care received; county and hospital of birth; information on the mother's reproductive history including number of previous pregnancies and live births; as well as statistics on the newborn and autopsy information.\n</p> <p>The data is strictly numerical, there is no identifying information given about the parents or child.</p>"
                  }
                }
              ]
            },
            {
              "typeName": "keyword",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "keywordValue": {
                    "typeName": "keywordValue",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "Births"
                  },
                  "keywordVocabulary": {
                    "typeName": "keywordVocabulary",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "ODUM:INDEX.TERMS"
                  }
                },
                {
                  "keywordValue": {
                    "typeName": "keywordValue",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "Infant death"
                  },
                  "keywordVocabulary": {
                    "typeName": "keywordVocabulary",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "ODUM:INDEX.TERMS"
                  }
                }
              ]
            },
            {
              "typeName": "notesText",
              "multiple": false,
              "typeClass": "primitive",
              "value": "Version Date: 1972Version Text: Birth/Infant Death"
            },
            {
              "typeName": "producer",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "producerName": {
                    "typeName": "producerName",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "State Center for Health Statistics"
                  },
                  "producerAbbreviation": {
                    "typeName": "producerAbbreviation",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "SCHS"
                  },
                  "producerURL": {
                    "typeName": "producerURL",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "http://www.schs.state.nc.us/SCHS/"
                  },
                  "producerLogoURL": {
                    "typeName": "producerLogoURL",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "http://www.schs.state.nc.us/SCHS/images/schslogo2.gif"
                  }
                }
              ]
            },
            {
              "typeName": "productionDate",
              "multiple": false,
              "typeClass": "primitive",
              "value": "1973"
            },
            {
              "typeName": "distributor",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "distributorName": {
                    "typeName": "distributorName",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "Odum Institute for Research in Social Science"
                  }
                }
              ]
            },
            {
              "typeName": "timePeriodCovered",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "timePeriodCoveredStart": {
                    "typeName": "timePeriodCoveredStart",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "1972-01-01"
                  },
                  "timePeriodCoveredEnd": {
                    "typeName": "timePeriodCoveredEnd",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "1972-12-31"
                  }
                }
              ]
            },
            {
              "typeName": "kindOfData",
              "multiple": true,
              "typeClass": "primitive",
              "value": [
                "Numeric"
              ]
            },
            {
              "typeName": "series",
              "multiple": false,
              "typeClass": "compound",
              "value": {
                "seriesName": {
                  "typeName": "seriesName",
                  "multiple": false,
                  "typeClass": "primitive",
                  "value": "North Carolina Vital Statistics"
                }
              }
            }
          ]
        },
        "geospatial": {
          "displayName": "Geospatial Metadata",
          "fields": [
            {
              "typeName": "geographicCoverage",
              "multiple": true,
              "typeClass": "compound",
              "value": [
                {
                  "country": {
                    "typeName": "country",
                    "multiple": false,
                    "typeClass": "controlledVocabulary",
                    "value": "United States"
                  }
                },
                {
                  "otherGeographicCoverage": {
                    "typeName": "otherGeographicCoverage",
                    "multiple": false,
                    "typeClass": "primitive",
                    "value": "North Carolina"
                  }
                }
              ]
            }
          ]
        }
      },
      "files": [
        {
          "description": "",
          "label": "guide.pdf",
          "version": 1,
          "datasetVersionId": 119,
          "datafile": {
            "id": 2514307,
            "name": "guide.pdf",
            "contentType": "application/pdf",
            "filename": "http://irss-arc1/dvn/dv/NCVITAL/FileDownload/guide.pdf?fileId=3160041",
            "originalFormatLabel": "UNKNOWN",
            "md5": "",
            "description": ""
          }
        },
        {
          "description": "",
          "label": "year_1968_to_1974_cdbk.pdf",
          "version": 1,
          "datasetVersionId": 119,
          "datafile": {
            "id": 2514309,
            "name": "year_1968_to_1974_cdbk.pdf",
            "contentType": "application/pdf",
            "filename": "http://irss-arc1/dvn/dv/NCVITAL/FileDownload/year_1968_to_1974_cdbk.pdf?fileId=3160038",
            "originalFormatLabel": "UNKNOWN",
            "md5": "",
            "description": ""
          }
        },
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
        {
          "description": "",
          "label": "year1972.sas.export",
          "version": 1,
          "datasetVersionId": 119,
          "datafile": {
            "id": 2514308,
            "name": "year1972.sas.export",
            "contentType": "application/octet-stream",
            "filename": "http://irss-arc1/dvn/dv/NCVITAL/FileDownload/year1972.sas.export?fileId=3160040",
            "originalFormatLabel": "UNKNOWN",
            "md5": "",
            "description": ""
          }
        },
        {
          "description": "",
          "label": "year1972.spss.tab",
          "version": 1,
          "datasetVersionId": 119,
          "datafile": {
            "id": 2514310,
            "name": "year1972.spss.tab",
            "contentType": "text/tab-separated-values",
            "filename": "http://irss-arc1/dvn/dv/NCVITAL/FileDownload/year1972.spss.tab?fileId=3160042",
            "originalFileFormat": "",
            "originalFormatLabel": "UNKNOWN",
            "UNF": "UNF:3:z0AXjpTw8XUM+nLVvQAFsQ==",
            "md5": "",
            "description": ""
          }
        }
      ]
    }
  }
}
"""
