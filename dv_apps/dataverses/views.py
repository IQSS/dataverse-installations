import StringIO
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.db.models import F
from dv_apps.dataverses.models import Dataverse
from dv_apps.utils.date_helper import get_timestamp_for_filename

# Create your views here.
def view_dataverse_list(request, output_format='xlsx', **kwargs):

    filter_params = {}

    published_only = kwargs.get('published_only', True)

    if published_only:
        filter_params.update(dict(dvobject__publicationdate__isnull=False))

    vals = ['id', 'name', 'alias', 'dataversetype', 'createdate', 'publicationdate' ]

    dlist = Dataverse.objects.select_related('dvobject'\
                ).filter(**filter_params
                ).annotate(id=F('dvobject__id'),
                    createdate=F('dvobject__createdate'),
                    publicationdate=F('dvobject__publicationdate'),
                ).values(*vals\
                ).order_by('alias')


    df = pd.DataFrame(list(dlist), columns=vals)

    df['dataverse_url'] = df['alias'].apply(lambda x: 'https://dataverse.harvard.edu/dataverse/%s' %  x)
    vals.append('dataverse_url')

    if output_format == 'xlsx':
        excel_string_io = StringIO.StringIO()

        pd_writer = pd.ExcelWriter(excel_string_io, engine='xlsxwriter')

        df.to_excel(pd_writer, index=False, sheet_name='metrics', columns=vals)

        pd_writer.save()

        excel_string_io.seek(0)
        workbook = excel_string_io.getvalue()

        if workbook is None:
            # Ah, make a better error
            return HttpResponse('Sorry! An error occurred trying to create an Excel spreadsheet.')


        xlsx_fname = 'dataverses_%s.xlsx' % get_timestamp_for_filename()

        response = HttpResponse(workbook,\
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response['Content-Disposition'] = 'attachment; filename=%s' % xlsx_fname

        return response

    return HttpResponse('Sorry.  This format is not recognized: %s' % output_format)
