# ------------------------------
# Quick script to add insitutions and
# affiliate them with dataverse installations
#
# Only deletes redundant institutions to refresh their affiliation
# ------------------------------
import os, sys
from os.path import isdir, realpath, isfile

proj_path = "../../../"
sys.path.append(proj_path)

# ------------------------------
# This is so Django knows where to find stuff.
# ------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniverse.settings.local")
import django
import re
django.setup()
from django.conf import settings
print settings.MEDIA_URL
from dv_apps.installations.models import Installation, Institution


def add_installations():
    """Add Institution information to the database"""

    # flat file -- replace with Google API
    fname = 'installation_data.txt'

    lines = open(fname, 'r').readlines()

    print 'installations:'

    _digits = re.compile('\d')
    def contains_digits(d):
        return bool(_digits.search(d))

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue    # go to the next line
        if (contains_digits(line) == False):
            continue
        # split line by a tab
        items = line.split('\t')
        #print items

        # skip items length != 3
        if len(items) != 3:
            continue

        name, lat, lng = items



        obj, created = Installation.objects.get_or_create(
            name = name,
            defaults = {'lat':lat, 'lng':lng}
        )

        #print obj, created
        if (created):
            print created, ",", name, "installation was created"
        else:
            print created, ",", name, "installation not created"


def add_institutions(source_file, dv_host_name='Harvard University'):
    """Add geocode institutions and associate them with the given installation"""

    if not isfile(source_file):
        print 'The source file was not found: %s' % source_file
        return

    # Retrieve the Dataverse installation
    #
    try:
        dv_host = Installation.objects.get(name=dv_host_name)
    except Installation.DoesNotExist:
        print 'Sorry, the installation [%s] was not found' % dv_host_name
        return

    # Read through the institution file
    #

    # Read file to array
    lines = open(source_file, 'r').readlines()

    # Remove blank lines
    lines = [x.strip() for x in lines if len(x.strip()) > 0]

    # Iterate through lines
    cnt = 0
    for line in lines:
        cnt+=1
        # split line by a tab
        items = line.split('\t')

        print '(%s) %s' % (cnt, items)
        # skip items length != 3  (no geocoding)
        if len(items) != 3:
            print '  - skipping, no geocoding'
            continue

        name, lat, lng = items

        # If it exists, delete the Institution
        # so it can be refreshed
        Institution.objects.filter(name=name).delete()

        #   Load the Institution object
        #
        info_dict = dict(lat=lat,\
                        lng=lng,\
                        host=dv_host)
        obj, created = Institution.objects.get_or_create(\
                name = name,\
                defaults = info_dict)

        if (created):
            print created, ",", name, "institution was created"
        else:
            print created, ",", name, "institution not created"

if __name__=='__main__':
    #add_installations()
    add_institutions('installation_txt_files/Harvard_University.txt')
