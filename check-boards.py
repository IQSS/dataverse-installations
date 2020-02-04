#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import csv
import json
import io

api_url_by_html_url = {}
iqss_projects_url = 'https://api.github.com/orgs/IQSS/projects'
req = Request(iqss_projects_url)
req.add_header('Accept', 'application/vnd.github.inertia-preview+json')
response = urlopen(req)
projects_out = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
for project in projects_out:
    html_url = project['html_url']
    api_url = project['url']
    api_url_by_html_url[html_url] = api_url

# Data maintained by IQSS.
iqss_url = 'https://docs.google.com/spreadsheets/d/1l2R9D1FQy88qVzg2bI6L1LgplmM2l7pnMI80jdiz4fk/export?gid=639378778&format=tsv'
response = urlopen(iqss_url)
iqss_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(iqss_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    hostname = row['Installation hostname']
    board_html_url = row['Project board under IQSS']
    if not board_html_url:
        continue
    board_api_url = row['Project board API URL']
    if not board_api_url:
        board_api_url = api_url_by_html_url[board_html_url]
        print(hostname + " created " + board_html_url + ' and "Project board API URL" should be updated to ' + board_api_url)
