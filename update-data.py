#!/usr/bin/env python3
import urllib.request as urlrequest
from urllib.parse import urlparse
import csv
import json
import io

mydict = {}

# Crowdsourced data.
crowd_url = 'https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/export?gid=0&format=tsv'
response = urlrequest.urlopen(crowd_url)
crowd_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(crowd_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    hostname = row['hostname']
    mydict[hostname] = {}
    launch_year = row['launch_year']
    if launch_year:
        mydict[hostname]['launch_year'] = launch_year
    else:
        mydict[hostname]['launch_year'] = None
    description = row['description']
    if description:
        mydict[hostname]['description'] = description
    else:
        mydict[hostname]['description'] = None

# Data maintained by IQSS.
iqss_url = 'https://docs.google.com/spreadsheets/d/1l2R9D1FQy88qVzg2bI6L1LgplmM2l7pnMI80jdiz4fk/export?gid=639378778&format=tsv'
response = urlrequest.urlopen(iqss_url)
iqss_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(iqss_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    hostname = row['Installation hostname']
    country = row['Country']
    continent = row['Continent']
    gdcc_member = row['GDCC member']
    board = row['Project board under IQSS']
    doi_authority = row['DOI authority']
    mydict[hostname]['country'] = country
    mydict[hostname]['continent'] = continent
    mydict[hostname]['gdcc_member'] = gdcc_member
    mydict[hostname]['board'] = board
    mydict[hostname]['doi_authority'] = doi_authority
    mydict[hostname]['contact_email'] = "UNKNOWN"

# Data about harvesting sets, etc.
harvest_url = 'https://docs.google.com/spreadsheets/d/12cxymvXCqP_kCsLKXQD32go79HBWZ1vU_tdG4kvP5S8/export?gid=0&format=tsv'
response = urlrequest.urlopen(harvest_url)
harvest_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(harvest_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    oai_url = row['OAI URL']
    o = urlparse(oai_url)
    hostname = o.hostname
    contact_email = row['Contact email']
    if contact_email:
        mydict[hostname]['contact_email'] = contact_email
    sets = row['Sets']
    if sets:
        mydict[hostname]['harvesting'] = sets
    else:
        mydict[hostname]['harvesting'] = None

# Data from dataverse.org/metrics (in version of Dataverse is new enough).
metrics_url = 'https://dataversemetrics.odum.unc.edu/dataverse-metrics/config.json'
response = urlrequest.urlopen(metrics_url)
metrics_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
metrics_list = []
for i in metrics_json['installations']:
    o = urlparse(i)
    hostname = o.hostname
    metrics_list.append(hostname)

# Data from miniverse map application.
miniverse_map_url = 'https://services.dataverse.harvard.edu/miniverse/map/installations-json'
response = urlrequest.urlopen(miniverse_map_url)
map_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
mylist = []
for i in map_json['installations']:
    foo = i
    o = urlparse(i['url'])
    i['hostname'] = o.hostname
    if i['hostname'] in metrics_list:
        i['metrics'] = True
    if i['hostname'] in mydict:
        if mydict[i['hostname']]['launch_year']:
            i['launch_year'] = mydict[i['hostname']]['launch_year']
        if mydict[i['hostname']]['description']:
            i['description'] = mydict[i['hostname']]['description']
        i['country'] = mydict[i['hostname']]['country']
        i['continent'] = mydict[i['hostname']]['continent']
        sets = mydict[i['hostname']].get('harvesting')
        if sets:
            all_sets = []
            for harvesting_set in sets.split(','):
                all_sets.append(harvesting_set.strip())
            i['harvesting_sets'] = all_sets
        is_gddc_member = False
        if mydict[i['hostname']]['gdcc_member'] == 'yes':
            is_gddc_member = True
        i['gdcc_member'] = is_gddc_member
        if mydict[i['hostname']]['doi_authority']:
            i['doi_authority'] = mydict[i['hostname']]['doi_authority']
        if mydict[i['hostname']]['board']:
            i['board'] = mydict[i['hostname']]['board']
        if mydict[i['hostname']]['contact_email'] != 'UNKNOWN':
            i['contact_email'] = mydict[i['hostname']]['contact_email']
    del i['id']
    del i['is_active']
    del i['slug']
    del i['full_name']
    del i['url']
    del i['version']
    del i['logo']
    mylist.append(i)

final = {}
final['installations'] = mylist
#print(json.dumps(final, indent=2))
json_out = 'data/data.json'
with open(json_out, 'w') as json_out:
    json.dump(final, json_out, indent=2)
