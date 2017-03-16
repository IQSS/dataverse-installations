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
        user_ids = []
        for model_name, type_id_list in get_dv_object_to_object_id_map().items():

            #   Get a list of object ids for this model type
            #   that were not emailed--e.g. should show up
            #   on the notifications pages
            #
            msgt('check: %s %s' % (model_name, type_id_list))
            model_user_id_list = UserNotification.objects.select_related('user'\
                                        ).filter(\
                                        object_type__in=type_id_list,
                                        ).values_list('objectid', 'user__id')

            model_id_list = [x[0] for x in model_user_id_list]

            user_ids += [x[1] for x in model_user_id_list]

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

        unique_user_ids = len(set(user_ids))

        return (broken_cnt, unique_user_ids)


        # Get notifications with

    @staticmethod
    def get_basic_stats():


        cnt_read_notifications = UserNotification.objects.filter(\
                                    readnotification=True,
                                    ).count()

        cnt_unread_notifications = UserNotification.objects.filter(\
                                    readnotification=False,
                                    ).count()

        cnt_undated_notifications = UserNotification.objects.filter(\
                                    senddate__isnull=True
                                    ).count()


        day_cnt_1 = 365
        day_cnt_1_date = datetime.now() - timedelta(days=day_cnt_1)

        day_cnt_2 = 180
        day_cnt_2_date = datetime.now() - timedelta(days=day_cnt_2)

        cnt_old_unread_notifications = UserNotification.objects.filter(\
                                    readnotification=False,
                                    senddate__lt=day_cnt_1_date
                                    ).count()

        cnt_old_unread_notifications2 = UserNotification.objects.filter(\
                                    readnotification=False,
                                    senddate__lt=day_cnt_2_date
                                    ).count()


        broken_cnt, impacted_users = NotificationStats.get_count_broken_notifications()
        msg('broken_cnt: %s' % broken_cnt)
        msg('impacted_users: %s' % impacted_users)


        file_stats = dict(\

            cnt_broken_notifications=NamedStat(\
                                'Broken Notifications / Impacted Users',
                                broken_cnt,
                                ('The notification refers to an object that'
                                 ' longer exists.  These notifications should'
                                 ' be deleted from the database. (May be'
                                 ' responsible for some users who receive an'
                                 ' error when clicking on the notifications'
                                 ' tab.)'),
                                None,
                                **dict(stat2=impacted_users)),

            cnt_read_notifications=NamedStat(\
                                'Read Notifications',
                                cnt_read_notifications,
                                ('Count of read notifications'),
                                None),

            cnt_unread_notifications=NamedStat(\
                                'All Unread Notifications',
                                cnt_unread_notifications,
                                ('Count of unread notifications.'),
                                None),

            cnt_unread_old_notifications=NamedStat(\
                                'Unread: Older than %s Days' % day_cnt_1,
                                cnt_old_unread_notifications,
                                ('Count of cnt_old_unread_notifications notifications and'
                                 ' notifications <b>older'
                                 ' than %d days</b>') % day_cnt_1,
                                None),

            cnt_old_unread_notifications2=NamedStat(\
                                'Unread: Older than %s Days' % day_cnt_2,
                                cnt_old_unread_notifications2,
                                ('Count of cnt_old_unread_notifications notifications and'
                                 ' notifications <b>older'
                                 ' than %d days</b>') % day_cnt_2,
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
