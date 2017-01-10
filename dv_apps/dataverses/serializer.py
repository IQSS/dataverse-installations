"""
Serialize a Dataverse object, similar to the native API:
    http://guides.dataverse.org/en/latest/api/native-api.html

Note: creator may be inaccurate.  These models assume it's an AuthenticatedUser
    - When is it not?  (e.g. group creates a Dataverse)
"""
from collections import OrderedDict

from django.forms.models import model_to_dict
from django.conf import settings

from dv_apps.dataverses.models import Dataverse, DataverseContact, DataverseTheme
from dv_apps.dataverses.util import DataverseUtil
from dv_apps.utils.date_helper import TIMESTAMP_MASK



class DataverseSerializer(object):
    """Serialize a Dataverse object, similar to the Dataverse native API"""

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


    def __init__(self, dataverse):
        assert isinstance(dataverse, Dataverse), "You must pass a Dataverse object!"

        # set the Dataverse
        self.dv = dataverse
        # set the DvObject
        self.dvobject = dataverse.dvobject


    def as_json(self):

        # -------------------------------
        # Serialize the basic Dataverse object
        # -------------------------------
        to_exclude = ['defaultcontributorrole', 'defaulttemplate', ]
        dv_dict = model_to_dict(self.dv, exclude=to_exclude)

        # -------------------------------
        # Set the id from th dvobject
        # -------------------------------
        dv_dict['id'] = dv_dict['dvobject']
        del dv_dict['dvobject']

        dv_dict['dv_link'] = DataverseUtil.get_dataverse_link(dv_dict['alias'])

        # -------------------------------
        # Set the contacts
        # -------------------------------
        dv_dict['contacts'] = self.get_contacts_list()

        # -------------------------------
        # Add attributes from the DvObject
        # -------------------------------

        # createDate
        #
        dv_dict['creationDate'] = self.dvobject.createdate.strftime(
        TIMESTAMP_MASK)

        # Owner
        #
        dv_dict['ownerInfo'] = OrderedDict()
        if self.dvobject.owner:
            dv_dict['ownerInfo']['ownerId'] = self.dvobject.owner.id
            dv_dict['ownerInfo']['isRootDataverse'] = False
            dv_dict['ownerInfo']['details'] = DataverseSerializer.get_short_dataverse_info(self.dvobject.owner)
        else:
            dv_dict['ownerInfo']['ownerId'] = None
            dv_dict['ownerInfo']['isRootDataverse'] = True


        # Creator
        #
        dv_dict['creator'] = OrderedDict()
        creator = self.dvobject.creator
        dv_dict['creator']['useridentifier'] = creator.useridentifier
        dv_dict['creator']['email'] = creator.email
        dv_dict['creator']['affiliation'] = creator.affiliation
        dv_dict['creator']['firstname'] = creator.firstname
        dv_dict['creator']['lastname'] = creator.lastname

        # -------------------------------
        # publication info
        # -------------------------------
        self.add_publication_info(dv_dict)

        # -------------------------------
        # add the theme
        # -------------------------------
        dv_dict['theme'] = self.get_dataverse_theme()

        # -------------------------------
        # order the keys based on KEY_ORDER1
        # -------------------------------
        fmt_dict = OrderedDict()
        for k in self.KEY_ORDER1:
            fmt_dict[k] = dv_dict.get(k, None)

        return fmt_dict

    @staticmethod
    def get_short_dataverse_info(owner_dvobject):
        """
        Get parent dataverse information
        """
        assert owner_dvobject is not None, "The DvObject (owner_dvobject) cannot be None"

        fmt_dict = OrderedDict()
        try:
            owner = Dataverse.objects.get(dvobject__id=owner_dvobject.id)
        except Dataverse.DoesNotExist:
            return fmt_dict

        fmt_dict['id'] = owner_dvobject.id
        fmt_dict['name'] = owner.name
        fmt_dict['alias'] = owner.alias
        fmt_dict['dv_link'] = DataverseUtil.get_dataverse_link(fmt_dict['alias'])
        fmt_dict['dv_link_json'] = DataverseUtil.get_dataverse_serialization_link(fmt_dict['alias'])
        fmt_dict['description'] = owner.description
        fmt_dict['dataversetype'] = owner.dataversetype
        return fmt_dict


    def add_publication_info(self, dv_dict):
        assert self.dvobject is not None, "The DvObject (self.dvobject) cannot be None"

        dv_dict['publicationInfo'] = OrderedDict()

        pub_date = self.dvobject.publicationdate
        if pub_date:
            dv_dict['publicationInfo']['isPublished'] = True
            dv_dict['publicationInfo']['publicationDate'] = pub_date.strftime(
            TIMESTAMP_MASK)
        else:
            dv_dict['publicationInfo']['isPublished'] = False

    def get_dataverse_theme(self):
        """
        Serialialize info found in the DataverseTheme table
        """
        assert self.dv is not None, "The Dataverse (self.dv) cannot be None"

        # Get the first theme
        # Looks like an error that there can be multiple themes...
        #
        theme = DataverseTheme.objects.filter(dataverse=self.dv).first()
        if theme is None:
            return None

        theme_dict = model_to_dict(theme)
        if theme_dict.has_key('logo'):
            logo_link = '%s/logos/%s/%s' % (settings.DATAVERSE_INSTALLATION_URL,
                        theme_dict.get('dataverse', None),
                        theme_dict['logo'])
            theme_dict['logo_link'] = logo_link

        return theme_dict

    def get_contacts_list(self):
        """
        Serialialize contacts found in the DataverseContact objects
        """
        assert self.dv is not None, "The Dataverse (self.dv) cannot be None"

        contacts = DataverseContact.objects.filter(dataverse=self.dvobject\
                    ).order_by('displayorder')

        fmt_list = []
        for contact in contacts:
            fmt_list.append(\
                        dict(email=contact.contactemail)\
                    )
        return fmt_list

"""
native API results as of 8/2016

"id": 8,
"alias": "PSI",
"name": "Population Services International (PSI)",
"affiliation": "Population Services International",
"dataverseContacts": [
  {
    "displayOrder": 0,
    "contactEmail": "research@psi.org"
  }
],
"permissionRoot": true,
"description": "PSI is a global health organization dedicated to improving the health of people in the developing world by focusing on serious challenges like a lack of family planning, HIV and AIDS, barriers to maternal health, and the greatest threats to children under five, including malaria, diarrhea, pneumonia and malnutrition.\r\n<br /><br />\r\nA hallmark of PSI is a commitment to the principle that health services and products are most effective when they are accompanied by robust communications and distribution efforts that help ensure wide acceptance and proper use.<br /><br />\r\n\r\nPSI works in partnership with local governments, ministries of health and local organizations to create health solutions that are built to last.",
"ownerId": 1,
"creationDate": "2013-08-20T18:55:24Z",
"creator": {
  "identifier": "@sonia",
  "displayInfo": {
    "Title": "Sonia Barbosa",
    "email": "sbarbosa@hmdc.harvard.edu"
  }
}
}
}"""
