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

# Crowdsourced information about Dataverse installations
crowd_url = 'https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/export?gid=0&format=tsv'
response = urlopen(crowd_url)
crowd_string = response.read().decode(response.info().get_param('charset') or 'utf-8')
reader = csv.DictReader(io.StringIO(crowd_string), delimiter="\t")
rows = [row for row in reader]
for row in rows:
    hostname = row['hostname']
    board_html_url = row['board']
    if not board_html_url:
        continue
    board_api_url = row['board_api']
    if not board_api_url:
        board_api_url = api_url_by_html_url[board_html_url]
        print(hostname + " created " + board_html_url + ' and "Project board API URL" should be updated to ' + board_api_url)
