# Contributing to dataverse-installations

Thank you for your interest in contributing to dataverse-installations!

### Everyone is welcome

We are open to contributions from everyone. You don't need to operate an installation of Dataverse to open issues or make suggestions. Please just go ahead! We welcome contributions of ideas, bug reports, feedback, documentation, code, and anything else you can think of.

## How the map works

The [update-data.py][] script downloads data from a [crowdsourced spreadsheet][] to construct a file called [data.json][] that contains lat/long coordinates and other information presented on the map at http://iqss.github.io/dataverse-installations

## Adding an installation to the map

First, create an issue with information about the installation.

Then, update the [crowdsourced spreadsheet][], requesting edit access if necessary.

Finally, run the update script and make a pull request. Python 3 is required.

`python3 update-data.py`

## Looking at the map locally

You can see the map at <http://localhost:8000> if you start a web server using the command below.

`python3 -m http.server`

### Coding style

`reformat-all.sh` is a script you can run from the root of the repo to format code but this is optional. We can always reformat code later.

## Security

If you would like to report a security issue, please email security@dataverse.org rather than creating an issue.

## Getting help

If you have questions or need help, please reach out at [chat.dataverse.org][] or the [dataverse-community Google Group][] or by creating an issue in the [issue tracker][].

[crowdsourced spreadsheet]: https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/edit#gid=0
[update-data.py]: update-data.py
[data.json]: data/data.json
[chat.dataverse.org]: http://chat.dataverse.org
[dataverse-community Google Group]: https://groups.google.com/group/dataverse-community
[issue tracker]: https://github.com/IQSS/dataverse-installations/issues
