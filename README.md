# dataverse-installations

dataverse-installations is the code that powers a map of [Dataverse][] installations around the world.

You can see the map at http://iqss.github.io/dataverse-installations

The map is populated by information about Dataverse installations in `data/data.json`

We need your help to update our data! Please see our [Contributing Guide][] for ways you can help.

[Dataverse]: https://dataverse.org
[Contributing Guide]: CONTRIBUTING.md
[spreadsheet maintained by IQSS]:https://docs.google.com/spreadsheets/d/1l2R9D1FQy88qVzg2bI6L1LgplmM2l7pnMI80jdiz4fk/edit?usp=sharing
[crowdsourced spreadsheet]: https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/edit#gid=0

## Viewing and Updating the map

**Requirements:**

**Python 3** OR **docker**

If the community has other ways, please let us know.


### To look at the map locally

If you just want to look at the map locally, download this repo and run 

`python3 -m http.server`

OR

`docker run --name dataverse-installations --rm -p 8000:8000 -v $PWD:/web -w /web -it python:3.7-alpine python3 -m http.server`


Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.


### To update the data shown on the map:
At this time, only the [crowdsourced spreadsheet] is editable by all. Any changes to the Crowdsourced spreadsheet will not automatically show up on the map. 

See full instructions on updating the information files as well as the map on the [Contributing Guide][]

## Map Data Sources (Inputs)
*Sherry is working on this*

## Outputs on the Map

The map is populated by information about Dataverse installations in `data/data.json` and here is where each field comes from:

| field | Source of truth |
| --- | --- |
| `name` | [spreadsheet maintained by IQSS][] |
| `description` | [crowdsourced spreadsheet][] |
| `launch_year` | [crowdsourced spreadsheet][] |
| `...` | ... |

The goal is to move as much information as possible to the [crowdsourced spreadsheet][].
