from __future__ import print_function
import datetime as dt
from collections import namedtuple
from decimal import Decimal

from django.db import connections
from django.conf import settings


from dv_apps.utils.byte_size import sizeof_fmt, comma_sep_number

from django.shortcuts import render
#from dv_apps.utils.message_helper_json import MessageHelperJSON
from django.http import JsonResponse, HttpResponse, Http404

from dv_apps.datafiles.models import Datafile
from django.db.models import Sum

from dv_apps.datafiles.s3_tier_utility import get_naive_price, bytes_to_gb
from django.views.decorators.cache import cache_page



def view_monthly_storage_info(selected_year=None):
    """List of download counts/bytes per mointh"""
    current_year = dt.datetime.now().year

    report_years = range(2014, current_year+1)

    if selected_year is None:
        selected_year = current_year

    assert str(selected_year).isdigit(),\
        'Not a valid year: %s (not digits)' % selected_year

    selected_year = int(selected_year)
    assert selected_year in report_years,\
        'Not a valid year: %s' % selected_year

    cursor = connections['dataverse'].cursor()

    sql_query = ("SELECT DATE_TRUNC('month', dv.createdate) AS month,"
                 " COUNT(df.id) AS added_count,"
                 " SUM(df.filesize) AS added_size"
                 " FROM dvobject dv, datafile df"
                 " WHERE dv.id = df.id"
                 " AND extract(YEAR from dv.createdate) = '%s'"
                 " GROUP BY date_trunc('month', dv.createdate)"
                 " ORDER BY month;") %\
                 (selected_year)
                 # where extract(YEAR from TIMESTAMP
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    fmt_rows = []
    storage_total_price = Decimal('0')
    total_files_added = Decimal('0')

    qs_sum_bytes = Datafile.objects.select_related('dvobject'\
                    ).filter(dvobject__createdate__year__lt=selected_year\
                    ).aggregate(Sum('filesize'))
    sum_bytes = qs_sum_bytes.get('filesize__sum')
    if sum_bytes is None:
        sum_bytes = Decimal('0')

    new_bytes_added = Decimal('0')

    fmt_rows = []
    for info in rows:
        info_list = list(info)
        print ('info_list', info_list)
        # Add comma separated # bytes
        info_list.append(comma_sep_number(info[2]))

        # Add monthly files to sum so far
        sum_bytes += info[2]
        new_bytes_added += info[2]

        # Add price as decimal
        monthly_price = get_naive_price(sum_bytes, '0.023')
        storage_total_price += monthly_price

        # Add price as string
        monthly_price_str = "{:,.2f}".format(monthly_price)

        info_dict = dict(month=info[0],
                         files_added=info[1],
                         bytes_added=info[2],
                         sum_bytes=sum_bytes,
                         monthly_price=monthly_price,
                         monthly_price_str=monthly_price_str,
                         total_files_added=total_files_added)

        fmt_rows.append(info_dict)

        total_files_added += info[1]

    report_years.reverse()

    return dict(storage_info=fmt_rows,
                storage_sum_bytes=sum_bytes,
                storage_new_bytes_added=new_bytes_added,
                storage_total_price=storage_total_price,
                storage_total_price_str="{:,.2f}".format(storage_total_price),
                total_files_added=total_files_added)
                #report_years=report_years,
                #selected_year=selected_year)


@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_monthly_downloads(request, selected_year=None):
    """List of download counts/bytes per mointh"""
    current_year = dt.datetime.now().year

    report_years = range(2014, current_year+1)

    if selected_year is None:
        selected_year = current_year

    if not str(selected_year).isdigit():
        raise Http404('Not a valid year: %s (not digits)' % selected_year)

    selected_year = int(selected_year)
    if selected_year not in report_years:
        raise Http404('Not a valid year: %s' % selected_year)


    cursor = connections['dataverse'].cursor()

    sql_query = ("SELECT DATE_TRUNC('month', gb.responsetime) AS month,"
                 " COUNT(gb.id) AS download_count,"
                 " SUM(df.filesize) AS download_size"
                 " FROM guestbookresponse gb, datafile df"
                 " WHERE gb.datafile_id = df.id"
                 " AND extract(YEAR from gb.responsetime) = '%s'"
                 " GROUP BY date_trunc('month', gb.responsetime)"
                 " ORDER BY month;") %\
                 (selected_year)
                 # where extract(YEAR from TIMESTAMP
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    fmt_rows = []
    total_bytes = Decimal('0')
    total_price = Decimal('0')
    total_download_count = Decimal('0')

    for info in rows:
        info_list = list(info)

        # Add comma separated # bytes
        info_list.append(comma_sep_number(info[2]))
        dec_price = get_naive_price(info[2])
        dec_price_str = "{:,.2f}".format(dec_price)

        # Add price as decimal
        info_list.append(dec_price)
        # Add price as string
        info_list.append(dec_price_str)

        # Add bytes as GB
        #info_list.append(bytes_to_gb(info[1]))

        fmt_rows.append(info_list)

        total_bytes += info[2]
        total_price += dec_price
        total_download_count += info[1]

    report_years.reverse()

    info_dict = dict(monthly_info=fmt_rows,
                     total_bytes=total_bytes,
                     total_price=total_price,
                     total_price_str="{:,.2f}".format(total_price),
                     total_download_count=total_download_count,
                     report_years=report_years,
                     selected_year=selected_year)

    info_dict.update(view_monthly_storage_info(selected_year))

    return render(request,
                  'datafiles/download_use.html',
                  info_dict)
