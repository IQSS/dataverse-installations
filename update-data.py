#!/usr/bin/env python3
import urllib.request as urlrequest
from urllib.parse import urlparse
import csv
import json
import io
import os

mydict = {}
mylist = []

# Data from dataverse.org/metrics (if version of Dataverse is new enough).
metrics_url = 'https://dataversemetrics.odum.unc.edu/dataverse-metrics/config.json'
response = urlrequest.urlopen(metrics_url)
metrics_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
metrics_list = []
for i in metrics_json['installations']:
    o = urlparse(i)
    hostname = o.hostname
    metrics_list.append(hostname)

# Crowdsourced data.
crowd_url = 'https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/export?gid=0&format=tsv'
response = urlrequest.urlopen(crowd_url)
crowd_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(crowd_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    skip = row['skip']
    if skip:
        continue
    hostname = row['hostname']
    name = row['name']
    mydict[hostname] = {}
    mydict[hostname]['name'] = name
    mydict[hostname]['description'] = row['description']
    latitude = float(row['latitude'])
    mydict[hostname]['lat'] = latitude
    longitude = float(row['longitude'])
    mydict[hostname]['lng'] = longitude
    mydict[hostname]['hostname'] = hostname
    if hostname in metrics_list:
        mydict[hostname]['metrics'] = True
    launch_year = row['launch_year']
    if launch_year:
        mydict[hostname]['launch_year'] = launch_year
    mydict[hostname]['country'] = row['country']
    mydict[hostname]['continent'] = row['continent']
    about_url = row['about_url']
    if about_url:
        mydict[hostname]['about_url'] = row['about_url']
    sets = row['harvesting_sets']
    if sets:
        all_sets = []
        for harvesting_set in sets.split(','):
            all_sets.append(harvesting_set.strip())
        mydict[hostname]['harvesting_sets'] = all_sets
    is_gddc_member = False
    if row['gdcc_member'] == 'yes':
        is_gddc_member = True
    mydict[hostname]['gdcc_member'] = is_gddc_member
    core_trust_seals = row['core_trust_seals']
    if core_trust_seals:
        all_seals = []
        for core_trust_seal in core_trust_seals.split(','):
            all_seals.append(core_trust_seal)
        mydict[hostname]['core_trust_seals'] = all_seals
    doi_authority = row['doi_authority']
    if doi_authority:
        mydict[hostname]['doi_authority'] = doi_authority
    board = row['board']
    if board:
        mydict[hostname]['board'] = board
    contact_email = row['contact_email']
    if contact_email:
        mydict[hostname]['contact_email'] = contact_email
    mylist.append(mydict[hostname])

final = {}
final['installations'] = sorted(mylist, key=lambda k: k['name'].lower())
json_out = os.path.join('data', 'data.json')
with open(json_out, 'w') as json_out:
    json.dump(final, json_out, indent=2)
