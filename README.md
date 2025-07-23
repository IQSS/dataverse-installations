# dataverse-installations

dataverse-installations is the code that powers a map of [Dataverse][] installations around the world.

You can see the map at https://dataverse.org/installations or http://iqss.github.io/dataverse-installations

## How the map works

The [update-data.py][] script downloads data from a [crowdsourced spreadsheet][] to construct a file called [data.json][] that contains lat/long coordinates and other information presented on the map.

## Contributing

If you see a problem in the [crowdsourced spreadsheet][], please go ahead and leave a comment and open an issue.

If you'd like to learn how to run the update script or work on the code, please see our [Contributing Guide][].

[Dataverse]: https://dataverse.org
[Contributing Guide]: CONTRIBUTING.md
[update-data.py]: update-data.py
[data.json]: data/data.json
[crowdsourced spreadsheet]: https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/edit#gid=0

## Editing the crowdsourced spreadsheet

If you are editing the [crowdsourced spreadsheet][], please note that we are transitioning the management of this file to the Dataverse Hub. In the meantime, we have added a new field called dv_hub_id. This ID will help us track all changes made to an installation.

Important Guidelines:

- Do not update an existing dv_hub_id. Once an ID has been used, it must remain unchanged.

- When adding a new installation, generate a new unique ID using the `uuidgen` command on Mac or Linux. On Windows, please use WSL (Windows Subsystem for Linux) to run the same command.