"""
Examine notifications, expecially those connected to objects
that no longer exist
"""
from dv_apps.notifications.models import UserNotification,\
        get_dv_object_to_object_id_map,\
        OBJECT_ID2TYPE_MAP
from dv_apps.quality_checks.named_stat import NamedStat
from dv_apps.dvobjects.models import DvObject
from dv_apps.dataverses.models import Dataverse
from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.dataverse_auth.models import AuthenticatedUser

from dv_apps.utils.msg_util import msg, msgt

from collections import Counter
from datetime import datetime, timedelta


class BrokenNotificationInfo(object):

    def __init__(self, model_name, model_user_id_list, missing_ids, **kwargs):
        """Calculate broken notificatin info"""

        assert model_name is not None, "model_name cannot be None"
        assert isinstance(model_user_id_list, list),\
            "model_user_id_list must be a list"
        assert isinstance(missing_ids, list),\
            "missing_ids must be a list"

        self.model_name = model_name
        self.missing_ids = missing_ids
        self.start_date = kwargs.get('start_date', None)

        # ------------------------------------------
        # Calculated attributes for *Broken* notifications
        # ------------------------------------------
        self.cnt_all_notifications = 0
        self.cnt_broken_notifications = 0
        self.percent_broken_string = None

        self.object_id_list = None
        self.cnt_unique_objects = 0

        self.user_id_list = None
        self.cnt_unique_users = 0

        self.notice_types = None
        # ------------------------------------------
        # Calculate attributes for *Broken* notifications
        # ------------------------------------------
        self.calculate_info(model_user_id_list)
        self.set_notice_types()

    def set_notice_types(self):
        """Return the types of notices associated with this model"""
        self.notice_types = []
        objects_ids = get_dv_object_to_object_id_map().get(self.model_name)
        assert objects_ids is not None,\
            "object_ids cannot be None for model name: %s" % self.model_name

        for obj_id in objects_ids:
            notice_type_name = OBJECT_ID2TYPE_MAP.get(obj_id, None)
            assert notice_type_name is not None,\
                ("notice_type_name cannot be for"
                 " id: %s\nSee 'OBJECT_ID2TYPE_MAP'") % obj_id

            self.notice_types.append(notice_type_name)

        self.notice_types.sort()

    def calculate_info(self, model_user_id_list):
        """
        Calculate counts/attributes
        model_id_list = [(object_id, user_id), (object_id, user_id), etc]
        """
        assert isinstance(model_user_id_list, list),\
            "model_user_id_list must be a list"

        self.cnt_all_notifications = len(model_user_id_list)

        broken_notices = [n for n in model_user_id_list if n[0] in self.missing_ids]
        self.cnt_broken_notifications = len(broken_notices)

        self.object_id_list = [n[0] for n in broken_notices]
        self.cnt_unique_objects = len(set(self.object_id_list))

        self.user_id_list = [n[1] for n in broken_notices]
        self.cnt_unique_users = len(set(self.user_id_list))

        float_percent = (self.cnt_broken_notifications + 0.0) / self.cnt_all_notifications
        self.percent_broken_string = '{0:.1%}'.format(float_percent)

    def get_user_list(self):
        """Return the AuthenticatedUser objects with notices
        that contain missing_ids"""
        assert self.user_id_list is not None,\
            "self.user_id_list cannot be None"

        return AuthenticatedUser.objects.filter(\
                        id__in=self.user_id_list\
                        ).distinct()


class NotificationStats(object):
    """Check for files without content types--or "unknown" content type"""
    def __init__(self, **kwargs):
        self.broken_info_list = []
        self.selected_model_name = kwargs.get('selected_model_name', None)
        self.load_broken_notifications()

    def load_broken_notifications(self):
        """Load broken notifications by type"""

        broken_notice_info = None
        for model_name, type_id_list in get_dv_object_to_object_id_map().items():
            #   Get a list of object ids for this model type
            #   that were not emailed--e.g. should show up
            #   on the notifications pages
            #
            msgt('check: %s %s' % (model_name, type_id_list))

            # If there's a selected_model_name, then only process that model
            #
            if self.selected_model_name is None:
                pass    # check all models
            elif model_name != self.selected_model_name:
                # We have a selected_model_name and this isn't it!
                continue

            model_user_id_list = UserNotification.objects.select_related('user'\
                                        ).filter(\
                                        object_type__in=type_id_list,
                                        ).values_list('objectid', 'user__id')

            if len(model_user_id_list) == 0:
                continue

            # retrieve the object ids only
            model_id_list = [x[0] for x in model_user_id_list]
            unique_id_list = list(set(model_id_list))

            # Next line is a hack - Need to upgrade Django apps
            #   to not use this method
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

            if len(unique_id_list) == len(existing_ids):
                # Looks good!
                # No notifications where object no longer exists
                continue

            # Create a list of the missing ids
            #
            missing_ids = list(set(unique_id_list) - set(existing_ids))

            # Record broken notification info
            #
            broken_notice_info = BrokenNotificationInfo(\
                                    model_name,
                                    list(model_user_id_list),
                                    missing_ids)
            self.broken_info_list.append(broken_notice_info)




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
                                 ' no longer exists.  These notifications should'
                                 ' be deleted from the database. (May be'
                                 ' responsible for some users who receive an'
                                 ' error when clicking on the notifications'
                                 ' tab.)'),
                                'view_broken_notifications',
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
                                ('Count of'
                                 ' notifications <b>older'
                                 ' than %d days</b>') % day_cnt_1,
                                None),

            cnt_old_unread_notifications2=NamedStat(\
                                'Unread: Older than %s Days' % day_cnt_2,
                                cnt_old_unread_notifications2,
                                ('Count of'
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
