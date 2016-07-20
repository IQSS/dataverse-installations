"""
Convenience methods for date formatting
"""
from datetime import datetime

DATE_DELIM = '-'

def format_yyyy_mm_dd(date_str, delim=DATE_DELIM):
    """Convert a string in YYYY-MM-DD format to a datetime object"""

    try:
        return True, datetime.strptime(date_str,\
            '%Y{0}%m{0}%d'.format(delim))
    except ValueError:
        return False, 'Date not in YYYY{0}MM{0}DD format'.format(DATE_DELIM)
