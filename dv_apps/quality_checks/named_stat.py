"""Convenience class for displaying data health info"""


class NamedStat(object):
    """Convenience class for displaying data health info"""

    def __init__(self, name, stat, desc=None, url_name=None, **kwargs):
        self.name = name
        self.stat = stat
        self.desc = desc
        self.url_name = url_name
        self.stat2 = kwargs.get('stat2', None)
