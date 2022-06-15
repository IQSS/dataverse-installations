#!/usr/bin/env python3
# For more context see https://github.com/pdurbin/druthers/issues/1
# First run boards2tsv.py to create boards.tsv.
# Then, in ~/.druthers/config.py put the following:
# api_token = 'PLACEHOLDER'
# The API token comes from https://github.com/settings/tokens
import csv
import sys
import os
from pathlib import Path
home = str(Path.home())
sys.path.append(home + os.sep + '.druthers')
import config
from urllib.request import Request, urlopen
import json
from urllib.parse import urlparse

def main():
    token = config.api_token
    tsv_file = 'boards.tsv'
    titles_by_issue = {}
    alldata = []
    with open(tsv_file) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        rows = [row for row in reader]
        for row in rows:
            board = row['Board URL HTML']
            board_json = row['Board URL JSON']
            print(board_json)
            project_id = board_json.split('/')[4]
            print(project_id)
            print(board)
            hostname = row['Installation hostname']
            print(hostname)
            boards_for_org_out  = '{}'
            boards_for_org_filename  = 'boards.json'
            columns_url = 'https://api.github.com/projects/' + project_id + '/columns'
            print('fetching ' + columns_url)
            columns_out = '{}'
            req = Request(columns_url)
            req.add_header('Accept', 'application/vnd.github.inertia-preview+json')
            req.add_header('Authorization', 'token ' + token)
            response = urlopen(req)
            columns_out = get_remote_json(response)
            columns = 'columns.json'
            for col in columns_out:
                cards_url = col['cards_url']
                column_name = col['name']
                print(cards_url)
                print('fetching ' + cards_url)
                req = Request(cards_url)
                req.add_header('Accept', 'application/vnd.github.inertia-preview+json')
                req.add_header('Authorization', 'token ' + token)
                response = urlopen(req)
                cards_out = get_remote_json(response)
                print( ' cards found in column ' + column_name)
                for card in cards_out:
                    mycard = {}
                    card_url = card.get('url', None)
                    content_url = card.get('content_url', None)
                    issue_url = None
                    archived = card['archived']
                    if content_url and not archived:
                        issue_org = content_url.split('/')[4]
                        issue_repo = content_url.split('/')[5]
                        issue_number = content_url.split('/')[7]
                        issue_url = 'https://github.com/' + issue_org + '/' + issue_repo + '/issues/' + issue_number
                    if issue_url:
                        datarow = []
                        datarow.append(issue_url)
                        datarow.append(hostname)
                        datarow.append(board)
                        datarow.append(column_name)
                        title = titles_by_issue.get(issue_url, None)
                        issue_state = ''
                        if not title:
                            api_issue_url = 'https://api.github.com/repos/' + issue_org + '/' + issue_repo + '/issues/' + issue_number
                            print('fetching ' + api_issue_url)
                            req = Request(api_issue_url)
                            req.add_header('Authorization', 'token ' + token)
                            response = urlopen(req)
                            issue_out = get_remote_json(response)
                            print(json.dumps(issue_out, indent=4))
                            titles_by_issue[issue_url] = issue_out['title']
                            title = titles_by_issue[issue_url]
                            issue_state = issue_out['state']
                        datarow.append(title)
                        if not issue_state == 'closed':
                            alldata.append(datarow)

    outfile = open('issues.tsv','w')
    writer=csv.writer(outfile, delimiter='\t')
    writer.writerow(['Issue URL', 'Installation hostname', 'Board URL', 'Board Column', 'Issue title'])
    alldata.sort(key=lambda x: x[0])
    writer.writerows(alldata)

def get_remote_json(response):
    return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

if __name__ == '__main__':
    main()
