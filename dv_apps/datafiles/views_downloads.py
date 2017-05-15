from __future__ import print_function
import datetime as dt
from collections import namedtuple
from decimal import Decimal

from django.db import connections
from dv_apps.utils.byte_size import sizeof_fmt, comma_sep_number

from django.shortcuts import render
from dv_apps.utils.message_helper_json import MessageHelperJSON
from django.http import JsonResponse, HttpResponse, Http404

from dv_apps.datafiles.models import Datafile

from django.conf import settings
from dv_apps.datafiles.s3_tier_utility import get_naive_price, bytes_to_gb


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
                 " GROUP BY date_trunc('month', gb.responsetime);") %\
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

    return render(request,
                  'datafiles/download_use.html',
                  info_dict)
