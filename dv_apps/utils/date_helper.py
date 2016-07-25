"""
Convenience methods for date formatting
"""
from datetime import datetime
import calendar
DATE_DELIM = '-'

def format_yyyy_mm_dd(date_str, delim=DATE_DELIM):
    """Convert a string in YYYY-MM-DD format to a datetime object"""

    try:
        return True, datetime.strptime(date_str,\
            '%Y{0}%m{0}%d'.format(delim))
    except ValueError:
        return False, 'Date not in YYYY{0}MM{0}DD format'.format(DATE_DELIM)

def get_month_name(month_num):
    """Convert a month integer, between 1 and 12, to a month name"""
    try:
        return True, calendar.month_name[month_num]
    except IndexError:
        return False, 'The month number must be between 1 and 12'
    except TypeError:
        return False, 'The month must be a *number* between 1 and 12'
    except:
        return False, 'The month must be a *number* between 1 and 12'
