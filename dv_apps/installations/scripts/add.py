# Only deletes redundant institutions to refresh their affiliation
#
#
#
#







import os, sys
from os.path import isdir, realpath

proj_path = "../"
sys.path.append(proj_path)

#sys.exit(0)
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Map_Database.settings")
import django
import re
django.setup()
from django.conf import settings
print settings.MEDIA_URL
from installations.models import Installation, Institution

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
        
print 'institutions:'

fname2 = 'institution_data.txt'
lines = open(fname2, 'r').readlines()
for line in lines:
    line = line.strip()
    
    if len(line) == 0:
        continue    # go to the next line

    # split line by a tab
    items = line.split('\t')
    #print items

    # skip items length != 3
    if len(items) != 3:
        continue

    name, lat, lng = items
    
    Institution.objects.filter(name=name).delete()
    
    inst = Installation.objects.filter(name=sys.argv[1])
    
    obj, created = Institution.objects.get_or_create(
        name = name,
        defaults = {'lat':lat, 'lng':lng, 'host':inst[0],}
    )
      
    #print obj, created
    if (created):
        print created, ",", name, "institution was created"
    else:
        print created, ",", name, "institution not created"
        
    #fmt_line = """%s is located at (%s, %s)""" % (name, lat, lng)

    #print fmt_line

    #formatted_items.append(fmt_line)

#open('output.txt', 'w').write('\n'.join(formatted_items))
