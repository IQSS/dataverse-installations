#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import csv
import json
import io

# Crowdsourced information about Dataverse installations
crowd_url = 'https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/export?gid=0&format=tsv'
response = urlopen(crowd_url)
crowd_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(crowd_string), delimiter="\t")
rows = [row for row in reader]

with open('boards.tsv', 'w', newline='') as tsvfile:
    output = csv.writer(tsvfile, delimiter='\t')
    header = [
        'Board URL HTML',
        'Board URL JSON',
        'Installation hostname',
    ]
    output.writerow(header)
    for row in rows:
        board_html_url = row['board']
        if not board_html_url:
            continue
        board_api_url = row['board_api']
        hostname = row['hostname']
        output.writerow([
            board_html_url,
            board_api_url,
            hostname,
        ])
