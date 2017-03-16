"""
Examine notifications, expecially those connected to objects
that no longer exist
"""
from dv_apps.notifications.models import UserNotification, get_dv_object_to_object_id_map
from dv_apps.quality_checks.named_stat import NamedStat
from dv_apps.dvobjects.models import DvObject
from dv_apps.dataverses.models import Dataverse
from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.utils.msg_util import msg, msgt

from collections import Counter
from datetime import datetime, timedelta

class NotificationStats(object):
    """Check for files without content types--or "unknown" content type"""
    def __init__(self):
        pass


    @staticmethod
    def get_count_broken_notifications():
        """
        Query each object type and make sure notifications aren't broken

        Example map
        { 'DvObject': [1],
          'Dataverse': [2],
          'Dataset': [14, 11], 'DatasetVersion': [13, 12, 7],
          'DataFile': [9]
         }

        """
        broken_cnt = 0
        for model_name, type_id_list in get_dv_object_to_object_id_map().items():

            #   Get a list of object ids for this model type
            #   that were not emailed--e.g. should show up
            #   on the notifications pages
            #
            msgt('check: %s %s' % (model_name, type_id_list))
            model_id_list = UserNotification.objects.filter(\
                                        #emailed=False,
                                        object_type__in=type_id_list,
                                        ).values_list('objectid', flat=True)

            msg('model_id_list len: %s' % len(model_id_list))
            if len(model_id_list) == 0:
                continue

            # Used for later "bad notice" counts
            notice_counter = Counter(model_id_list)
            msg('notice_counter len: %s' % len(notice_counter))

            unique_id_list = list(set(model_id_list))
            msg('unique_id_list len: %s' % len(unique_id_list))

            # Need to upgrade apps files and not use this method
            model_class = eval(model_name)
            if model_name in ['DvObject', 'DatasetVersion', 'FileMetadata']:
                existing_ids = model_class.objects.filter(id__in=unique_id_list\
                                            ).values_list('id', flat=True\
                                            ).distinct()
            else:
                existing_ids = model_class.objects.select_related('dvobject'\
                                    ).filter(dvobject__id__in=unique_id_list\
                                    ).values_list('dvobject__id', flat=True\
                                    ).distinct()

            msg('existing_ids len: %s' % len(existing_ids))

            if len(unique_id_list) == len(existing_ids):
                # Looks good!
                continue

            missing_ids = list(set(unique_id_list) - set(existing_ids))
            for missing_id in missing_ids:
                broken_cnt += notice_counter.get(missing_id, 0)

        return broken_cnt


        # Get notifications with

    @staticmethod
    def get_basic_stats():


        """cnt_read_notifications = UserNotification.objects.filter(\
                                    readnotification=True,
                                    ).count()
        """
        cnt_unread_notifications = UserNotification.objects.filter(\
                                    readnotification=False,
                                    ).count()

        cnt_undated_notifications = UserNotification.objects.filter(\
                                    senddate__isnull=True
                                    ).count()




        day_cnt = 365
        one_year_old = datetime.now() - timedelta(days=day_cnt)


        cnt_old_unread_notifications = UserNotification.objects.filter(\
                                    readnotification=False,
                                    senddate__lt=one_year_old
                                    ).count()


        file_stats = dict(\

            cnt_broken_notifications=NamedStat(\
                                'Broken Notifications',
                                NotificationStats.get_count_broken_notifications(),
                                ('The notification refers to an object that'
                                 ' longer exists--should be deleted from db'),
                                None),

            cnt_unread_notifications=NamedStat(\
                                'Unread Notifications',
                                cnt_unread_notifications,
                                ('Count of unread notifications'),
                                None),

            cnt_old_unread_notifications=NamedStat(\
                                'Old Unread Notifications',
                                cnt_old_unread_notifications,
                                ('Count of unread notifications older'
                                 ' than %d days') % day_cnt,
                                None),

            cnt_undated_notifications=NamedStat(\
                                'Undated Notifications',
                                cnt_undated_notifications,
                                ('Count of undated notifications'),
                                None),
            #cnt_harvested_zero=NamedStat(\
            #                    'Filesize 0 (Harvested)',
            #                    cnt_harvested_zero,
            #                    ('Count of harvested Datafiles displaying a'
            #                     ' size of 0 bytes')),
            )

        return file_stats
