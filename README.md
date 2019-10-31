# dataverse-installations

dataverse-installations is the code that powers a map of [Dataverse][] installations around the world.

You can see the map at http://iqss.github.io/dataverse-installations

The map is populated by information about Dataverse installations in `data/data.json` and here is where each field comes from:

| field | Source of truth |
| --- | --- |
| `name` | [spreadsheet maintained by IQSS][] |
| `description` | [crowdsourced spreadsheet][] |
| `launch_year` | [crowdsourced spreadsheet][] |
| `...` | ... |

The goal is to move as much information as possible to the [crowdsourced spreadsheet][].

We love contributors! Please see our [Contributing Guide][] for ways you can help.

[Dataverse]: https://dataverse.org
[Contributing Guide]: CONTRIBUTING.md
[spreadsheet maintained by IQSS]:https://docs.google.com/spreadsheets/d/1l2R9D1FQy88qVzg2bI6L1LgplmM2l7pnMI80jdiz4fk/edit?usp=sharing
[crowdsourced spreadsheet]: https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/edit#gid=0

## with docker

`docker-compose up -d ` and go to [http://127.0.0.1/](http://127.0.0.1/).

To run python command : `docker-compose exec cmd python update-data.py`