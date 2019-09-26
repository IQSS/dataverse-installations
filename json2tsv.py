#!/usr/bin/env python3
import urllib.request as urlrequest
import json
import csv
onmap = 'https://services.dataverse.harvard.edu/miniverse/map/installations-json'
response = urlrequest.urlopen(onmap)
map_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
installations = map_json['installations']
with open('dataverse-installations.tsv', 'w', newline='') as tsvfile:
    output = csv.writer(tsvfile, delimiter='\t')
    output.writerow(installations[0].keys())  # header row
    for i in installations:
        output.writerow(i.values())
