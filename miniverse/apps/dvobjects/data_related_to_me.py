from django.db import connection


class DataRelatedToMe(object):

    def __init__(self, username):

        self.username = username
        self.role_lookup = {}   # { role_id : name }

        self.direct_role_assignments = []
        self.direct_dvobject_assignments = []

        # -----------------------
        # dataverses
        # -----------------------
        self.dataverse_info = []
        self.all_dataverse_ids = []

        # -----------------------
        # datasets
        # -----------------------
        self.dataset_info = []
        self.initial_dataset_ids = []
        self.secondary_dataset_ids = []

        # -----------------------
        # datafiles
        # -----------------------
        self.file_info = []
        self.initial_file_ids = []
        self.secondary_file_ids = []

        # -----------------------
        self.err_msg = None
        self.err_found = False

        self.load_roles()
        self.load_dvobject_info()

    def get_total_object_count(self):

        return len(self.get_dataverse_ids())\
               + len(self.get_dataset_ids())\
               + len(self.get_file_ids())

    def get_dataverse_ids(self):
        """Get unique dataverse ids"""
        return set(self.all_dataverse_ids)

    def get_dataset_ids(self):
        """Get unique Dataset ids"""
        return set(self.initial_dataset_ids + self.secondary_dataset_ids)

    def get_file_ids(self):
        """Get unique DataFile ids"""
        return set(self.initial_file_ids + self.secondary_file_ids)

    def load_roles(self):

        q = """SELECT name, id, description FROM dataverserole ORDER by id;"""
        self.role_query = q
        role_query_results = self.get_query_results(q)

        for qr in role_query_results:
            self.role_lookup[qr['id']] = qr['name']

        #d.update(dict(role_query=role_query, role_query_results=role_query_results))


    def load_dvobject_info(self):

        if not self.step1_load_direct_assignments():
            return

        if not self.step2_load_direct_dv_objects():
            return

        self.step3_load_indirect_dataset_info()

        self.step_load4_indirect_file_info()


    def step_load4_indirect_file_info(self):

        if len(self.initial_dataset_ids) == 0 and len(self.secondary_dataset_ids) == 0:
            return

        dataset_ids_as_str = [ str(x) for x in (self.initial_dataset_ids + self.secondary_dataset_ids)]

        q = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
FROM dvobject dv
WHERE dv.owner_id IN (%s)
AND dv.dtype IN ('DataFile');
""" % (','.join(dataset_ids_as_str ),
      )
        self.secondary_file_query = q

        qresults = self.get_query_results(q)
        if qresults is None or len(qresults)==0:
            return

        # May overlap with initial datafile_ids and info
        self.secondary_file_ids = [ x['id'] for x in qresults]
        self.file_info.append(qresults)



    def step3_load_indirect_dataset_info(self):
        """If the user has Dataverse assignments, look for underlying Datasets"""

        if self.all_dataverse_ids is None or len(self.all_dataverse_ids) == 0:
            return

        dataverse_ids_as_str = [ str(x) for x in self.all_dataverse_ids]

        q = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
FROM dvobject dv
WHERE dv.owner_id IN (%s)
AND dv.dtype IN ('Dataset');
""" % (','.join(dataverse_ids_as_str ),
      )
        self.secondary_dataset_query = q

        qresults = self.get_query_results(q)
        if qresults is None or len(qresults)==0:
            return

        # May overlap with initial dataset_ids and info
        self.secondary_dataset_ids = [ x['id'] for x in qresults]
        self.dataset_info.append(qresults)


    def step2_load_direct_dv_objects(self):

        assert self.dv_object_ids is not None and len(self.dv_object_ids) > 0, 'You must have dv_object_ids'

        dv_ids_as_strings = [ str(x) for x in self.dv_object_ids]

        q = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
FROM dvobject dv
WHERE dv.id IN (%s)
ORDER BY dv.dtype;""" % ','.join(dv_ids_as_strings)

        self.dvobject_query = q

        qresults = self.get_query_results(q)
        if qresults is None or len(qresults)==0:
            self.add_err_msg('No direct dv objects found.')
            return False

        self.direct_dvobject_assignments = qresults

        # Parse out Dataverse information (complete)
        #
        self.dataverse_info = [ x for x in qresults if x['dtype'] == 'Dataverse']
        self.all_dataverse_ids = [ x['id'] for x in self.dataverse_info]

        # Parse out Dataset information (incomplete)
        #
        self.dataset_info = [ x for x in qresults if x['dtype'] == 'Dataset']
        self.initial_dataset_ids = [ x['id'] for x in self.dataset_info]

        # Parse out File information (incomplete)
        #
        self.file_info = [ x for x in qresults if x['dtype'] == 'DataFile']
        self.initial_file_ids = [ x['id'] for x in self.file_info]
        print 'initial_file_ids', len(self.initial_file_ids)
        return True

    def step1_load_direct_assignments(self):
        """
        Pull Info for Directly Assigned Objects
        """
        q = """SELECT r.id, r.assigneeidentifier, r.definitionpoint_id, r.role_id
FROM roleassignment r
WHERE substr(r.assigneeidentifier, 2)= '%s';""" % (self.username,)

        self.assign_query = q

        qresults = self.get_query_results(q)
        if qresults is None or len(qresults)==0:
            self.add_err_msg('No direct role assignments found.')
            return False

        self.direct_role_assignments = qresults
        self.dv_object_ids =  [ x['definitionpoint_id'] for x in qresults]


        return True


    def add_err_msg(self, m):
        self.err_found = True
        self.err_msg = m


    def get_query_results(self, query_str):

        cursor = connection.cursor()

        cursor.execute(query_str)

        return self.dictfetchall(cursor)


    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
