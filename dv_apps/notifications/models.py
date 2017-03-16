from __future__ import unicode_literals
from dv_apps.dataverse_auth.models import AuthenticatedUser
from django.db import models

OBJECT_ID2TYPE_MAP = {\
        0 : 'ASSIGNROLE',
		1 : 'REVOKEROLE',
		2 : 'CREATEDV',
		3 : 'CREATEDS',
		4 : 'CREATEACC',
		5 : 'MAPLAYERUPDATED',
		6 : 'SUBMITTEDDS',
		7 : 'RETURNEDDS',
		8 : 'PUBLISHEDDS',
		9 : 'REQUESTFILEACCESS',
		10 : 'GRANTFILEACCESS',
		11 : 'REJECTFILEACCESS',
		12 : 'FILESYSTEMIMPORT',
		13 : 'CHECKSUMIMPORT',
		14 : 'CHECKSUMFAIL'}

# reverse the map above
OBJECT_TYPE2ID_MAP = dict([(v, k) for k, v in OBJECT_ID2TYPE_MAP.items()])

OBJECT_TYPE_TO_DVOBJECT_MAP = dict(\
        ASSIGNROLE=None,
        REVOKEROLE='DvObject',
        CREATEDV='Dataverse',
        CREATEDS='DatasetVersion',
        MAPLAYERUPDATED='FileMetadata',
        REQUESTFILEACCESS='DataFile',
        GRANTFILEACCESS=None,
        REJECTFILEACCESS='Dataset',
        RETURNEDDS='DatasetVersion',
        CHECKSUMFAIL='Dataset',
        FILESYSTEMIMPORT='DatasetVersion',
        CHECKSUMIMPORT='DatasetVersion',)

def get_dv_object_to_object_id_map():
    """Map of { modelName : [type id, type id, etc.]}

    e.g. { 'Dataset' : [11, 14]}
    """
    reverse_map = dict()

    for k, v in OBJECT_TYPE_TO_DVOBJECT_MAP.items():
        val = OBJECT_TYPE2ID_MAP.get(k, None)
        if v and val:
            reverse_map.setdefault(v, []).append(val)

    return reverse_map



class UserNotification(models.Model):
    """User notifications"""
    emailed = models.NullBooleanField()

    readnotification = models.NullBooleanField()

    object_type = models.IntegerField(db_column='type')
    objectid = models.BigIntegerField(blank=True, null=True)
    senddate = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(AuthenticatedUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usernotification'

    @staticmethod
    def get_object_model_name(object_type_id):
        """Based on DataverseUserPage.java displayNotification()"""
        object_type_name = OBJECT_TYPE_MAP.get(object_type_id, None)
        if object_type_name is None:
            return None

        if object_type_name == 'ASSIGNROLE':
            # no associated object
            return None

        elif object_type_name == 'REVOKEROLE':
            # can be dataverse, dataset, or file
            return 'DvObject'

        elif object_type_name == 'CREATEDV':
            return 'Dataverse'

        elif object_type_name == 'REQUESTFILEACCESS':
            return 'DataFile'

        elif object_type_name == 'GRANTFILEACCESS':
            return None

        elif object_type_name == 'REJECTFILEACCESS':
            return 'Dataset'

        elif object_type_name == 'RETURNEDDS':
            return 'DatasetVersion'

        elif object_type_name == 'CHECKSUMFAIL':
            return 'Dataset'

        elif object_type_name == 'FILESYSTEMIMPORT':
            return 'DatasetVersion'

        elif object_type_name == 'CHECKSUMIMPORT':
            return 'DatasetVersion'

        else:
            return None
