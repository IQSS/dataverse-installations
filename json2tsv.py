#!/usr/bin/env python3
import json
import csv
with open('data/data.json', 'r') as json_file:
    json_data=json_file.read()
installations = json.loads(json_data)['installations']
with open('dataverse-installations.tsv', 'w', newline='') as tsvfile:
    output = csv.writer(tsvfile, delimiter='\t')
    header = [
        'name',
        'country',
        'launch_year',
        'hostname',
        'continent',
        'latitude',
        'longitude',
        'about_url',
        'description',
    ]
    output.writerow(header)
    for i in installations:
        name = i['name']
        country = i['country']
        launch_year = i.get('launch_year', None)
        continent = i['continent']
        hostname = i['hostname']
        latitude = i['lat']
        longitude = i['lng']
        about_url = i.get('about_url', None)
        description = i['description']
        output.writerow([
            name,
            country,
            launch_year,
            hostname,
            continent,
            latitude,
            longitude,
            about_url,
            description,
        ])
