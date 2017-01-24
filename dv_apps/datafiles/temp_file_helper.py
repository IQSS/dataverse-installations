import os
from os.path import isfile
import tempfile
import requests
from dv_apps.utils.msg_util import msg, msgt

"""
# https://dataverse.harvard.edu/api/access/datafile/2971583
tf = tempfile.NamedTemporaryFile()
#tf.name  # retrieve the name of the temp file just created
with TemporaryFile() as f:
    f.write('abcdefg')
    f.seek(0)  # go back to the beginning of the file
    print(f.read())
"""

def download_file(url_to_file):
    """Download a Dataverse file and return the filename"""

    file_handle, filepath = tempfile.mkstemp()

    msgt('download file: %s' % url_to_file)

    r = requests.get(url_to_file, stream=True)

    if r.status_code != 200:
        msg('bad status: %s' % r.status_code)
        if isfile(filepath):
            make_sure_file_deleted(filepath)
        return None

    with os.fdopen(file_handle, 'wb') as tmp:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                tmp.write(chunk)

    msg('File downloaded: %s' % filepath)
    return filepath


def make_sure_file_deleted(filepath):
    assert filepath is not None, 'filepath cannot be None'

    if isfile(filepath):
        os.remove(filepath)
        return True

    return True

'''
fd, path = tempfile.mkstemp()
try:
    with os.fdopen(fd, 'w') as tmp:
        # do stuff with temp file
        tmp.write('stuff')
finally:
    os.remove(path)
'''
