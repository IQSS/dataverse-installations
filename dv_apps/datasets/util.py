"""


import requests
dv_ids = [5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 51, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 101, 102, 104, 105]

ds_ids = [46587, 46589, 46590, 46598, 46603, 46612, 46630, 46652, 46657, 46671, 46675, 46700, 46735, 46744, 46768, 46783, 46784, 46794, 46808, 46832, 46839, 46877, 46892, 46893, 46912, 46928, 46929, 46938, 46955, 46958, 47001, 47018, 47022, 47037, 47051, 47066, 47069, 47078, 47080, 47081, 47097, 47112, 47130, 47152, 47169, 47172, 47191, 47220, 47259, 47294]

url = 'https://dataverse.harvard.edu/api/datasets/4118'
url = '127.0.0.1:8000/dvobjects/api/v1/dataverses/8'


demo_dv_ids = [1, 2, 3, 4, 5, 6, 7, 27, 41, 48, 55, 60, 70, 84, 116, 119, 120, 121, 122, 127, 135, 142, 143, 150, 152, 159, 162, 166, 170, 171, 176, 179, 181, 185, 186, 187, 193, 196, 197, 205, 247, 253, 262, 269, 279, 283, 287, 293, 303, 305, 347, 352, 353, 354, 355, 363, 364, 365, 366, 368, 369, 380, 388, 394, 398, 399, 417, 427, 428, 436, 465, 497, 502, 505, 511, 524, 528, 531, 532, 537, 538, 541, 542, 544, 545, 546, 547, 548, 550, 551, 552, 554, 555, 559, 583, 584, 585, 588, 594, 598, 621, 626, 627, 636, 645, 653, 656, 663, 668, 675, 684, 685, 689, 692, 821, 824, 829, 830, 831, 837, 865, 1066, 1075, 1076, 1089, 1090, 1091, 1093, 1108, 1113, 1116, 1123, 1125, 1130, 1145, 1148, 1153, 1157, 1160, 1183, 1188, 1191, 1200, 1201, 1204, 1207, 1210, 1216, 1230, 1243, 1270, 1282, 1286, 1287, 1290, 1298, 1307, 1310, 1324, 1327, 1331, 1348, 1353, 1356, 1361, 1365, 1367, 1369, 1372, 1373, 1374, 1397, 1398, 1399, 1401, 1409, 1410, 1424, 1431, 1438, 1453, 1456, 1457, 1460, 1463, 1466, 1467, 1470, 1473, 1474, 1591, 1597, 1601, 1611, 1612, 1617, 1620, 1626, 1638, 1641, 1653, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1693, 1694, 1700, 1701, 1705, 1712, 1713, 1714, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1735, 1742, 1749, 1753, 1764, 1773, 1776, 1777, 1778, 1779, 1780, 1826, 1827, 1896, 1898, 2007, 2016, 2109, 2110, 2116, 2121, 2122, 2125, 2133, 2139, 2149, 2160, 2170, 2174, 2194, 2199, 2203, 2205, 2206, 2214, 2219, 2244, 2253, 2275, 2276, 2277, 2278, 2384, 2385, 2393, 2403, 2404, 2406, 2416, 2421, 2436, 2441, 2442, 2447, 2451, 2457, 2467, 2472, 2475, 2478, 2481, 2484, 2492, 2497, 2501, 2537, 2559, 2573, 2576, 2582, 2587, 2590, 2592, 2598, 2599, 2602, 2607, 2663, 2686, 2695, 2700, 2706, 2712, 2714, 2720, 2725, 2734, 2742, 2759, 2845, 2858, 3004, 3005, 3006, 3011, 3018, 3024, 3025, 3055, 3063, 3076, 3085, 3087, 3089, 3099, 3101, 3104, 3105, 3112, 3153, 3174, 3179, 3188, 3189, 3307, 3308, 3319, 3411, 3423, 3425, 3438, 4411, 4414, 4416, 4421, 4422, 4425, 4439, 4933, 4934, 5044, 5537]

def run_api_call(metrics=False, limit=100):
    cnt = 0
    for id in demo_dv_ids in dv_ids:
        cnt += 1

        # format url
        #
        if metrics:
            url = 'https://services-dataverse.herokuapp.com/dvobjects/api/v1/dataverses/%s' % id
        else:
            url = 'https://demo.dataverse.org/api/dataverses/%s' % id


        # make the call
        #
        print '(%d) %s' % (cnt, url)
        r = requests.get(url)
        print r.status_code

        if cnt == limit:
            break

run_api_call()

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
