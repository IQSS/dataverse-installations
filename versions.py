#!/usr/bin/env python3
import urllib.request as urlrequest
import json
from urllib.parse import urlparse
onmetrics = 'https://dataversemetrics.odum.unc.edu/dataverse-metrics/config.json'
response = urlrequest.urlopen(onmetrics)
metrics_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
onmap = 'https://services.dataverse.harvard.edu/miniverse/map/installations-json'
response = urlrequest.urlopen(onmap)
map_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
for i in map_json['installations']:
    url = i['url']
    o = urlparse(url)
    hostname = o.netloc
    basename = 'https://' + hostname
    polled = False
    if basename in metrics_json['installations']:
        polled = True
    version_url = basename + '/api/info/version'
    try:
        response = urlrequest.urlopen(version_url)
        json_out = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        version = json_out['data']['version']
        print(basename, version, polled)
    except:
        print(basename, 'UNKNOWN', polled)
