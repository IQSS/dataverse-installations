#!/usr/bin/env python3
import json
with open('data/data.json', 'r') as json_file:
    json_data=json_file.read()
installations = json.loads(json_data)['installations']
for i in installations:
    board = i.get('board', None)
    if not board:
        continue
    name = i['name']
    print('- ' + name + ": " + board)
