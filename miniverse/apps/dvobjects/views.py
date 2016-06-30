from django.db import connection
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from data_related_to_me import DataRelatedToMe
from .forms import FilterForm

# Create your views here.
def view_test_query(request, username=None):

    if username is None:
        username = 'garyking'

    f = FilterForm()

    d = dict(username=username, d2me=DataRelatedToMe(username=username),
             filter_form=f)

    return render_to_response('miniverse/test_query.html', d)



# Create your views here.
def xview_test_query(request, username=None):

    if username is None:
        username = 'garyking'


    d = dict(username=username, d2me=DataRelatedToMe(username=username))

    # --------------------------------------
    # role description query
    # --------------------------------------
    role_query = """SELECT name, id, description FROM dataverserole ORDER by id;"""
    role_query_results = get_query_results(role_query)
    d.update(dict(role_query=role_query, role_query_results=role_query_results))

    # --------------------------------------
    # role assignments query
    # --------------------------------------
    assign_query = """SELECT r.id, r.assigneeidentifier, r.definitionpoint_id, r.role_id
FROM roleassignment r
WHERE substr(r.assigneeidentifier, 2)= '%s';""" % (username,)
    assign_query_results = get_query_results(assign_query)
    d.update(dict(assign_query=assign_query, assign_query_results=assign_query_results))

    # Retrieve dvobject ids from query
    dv_ids = [ x['definitionpoint_id'] for x in assign_query_results]

    if len(dv_ids) == 0:
        return HttpResponse('no assignments')
    dv_ids_as_strings = [ str(x) for x in dv_ids]



    # --------------------------------------
    # dvobject query - DIRECT ASSIGNMENTS
    # --------------------------------------
    dvobject_query = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
FROM dvobject dv
WHERE dv.id IN (%s)
ORDER BY dv.dtype;""" % ','.join(dv_ids_as_strings)

    dvobject_query_results = get_query_results(dvobject_query)
    d.update(dict(dvobject_query=dvobject_query, dvobject_query_results=dvobject_query_results),
             dv_ids_as_strings=dv_ids_as_strings)

    # Dataverse IDs
    dataverse_ids = [x['id'] for x in dvobject_query_results if x['dtype']=='Dataverse']
    num_dataverses = len(dataverse_ids)

    # Dataset IDs
    dataset_ids = [x['id'] for x in dvobject_query_results if x['dtype']=='Dataset']
    num_datasets = len(dataset_ids)

    # Files
    datafile_ids = [x['id'] for x in dvobject_query_results if x['dtype']=='DataFile']
    num_files = len([x for x in dvobject_query_results if x['dtype']=='DataFile'])

    d.update(dict(num_dataverses=num_dataverses, num_datasets=num_datasets, num_files=num_files))

    # --------------------------------------
    # Data query - INDIRECT Datasets
    # --------------------------------------
    parent_dataverse_ids = [str(x) for x in dataverse_ids]

    secondary_dataset_query = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
FROM dvobject dv
WHERE dv.owner_id IN (%s)
AND dv.dtype IN ('Dataset')
ORDER BY dv.dtype;
""" % (','.join(parent_dataverse_ids ),
      )

    secondary_dataset_query_results = get_query_results(secondary_dataset_query)

    d.update(dict(secondary_dataset_query=secondary_dataset_query,
                  secondary_dataset_query_results=secondary_dataset_query_results))

    # --------------------------------------
    # Data query - INDIRECT ASSIGNMENTS - FILES
    # --------------------------------------
    secondary_parent_dataset_ids = [x['id'] for x in secondary_dataset_query_results if x['dtype']=='Dataset']
    parent_dataset_ids = [str(x) for x in (dataset_ids + secondary_parent_dataset_ids)]

    secondary_file_query = """SELECT dv.id, dv.dtype, dv.modificationtime, dv.owner_id
 FROM dvobject dv
 WHERE dv.owner_id IN (%s)
 AND dv.dtype = 'DataFile'
 ORDER BY dv.dtype;
""" % (','.join(parent_dataset_ids),
       )

    secondary_file_query_results = get_query_results(secondary_file_query)

    d.update(dict(secondary_file_query=secondary_file_query,
                  secondary_file_query_results=secondary_file_query_results))


    return render_to_response('miniverse/test_query.html', d)
    return HttpResponse('hi')



def get_query_results(query_str):

    cursor = connection.cursor()

    cursor.execute(query_str)

    return dictfetchall(cursor)


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
