# Contributing to dataverse-installations

Thank you for your interest in contributing to dataverse-installations!

### Everyone is welcome

We are open to contributions from everyone. You don't need to operate an installation of Dataverse to open issues or make suggestions. Please just go ahead! We welcome contributions of ideas, bug reports, feedback, documentation, code, and anything else you can think of.

## Ways to Contribute
The map of dataverse installations around the world is created from two files that contain various bits of info on each dataverse installations, [crowdsourced spreadsheet][] and the more detailed [spreadsheet maintained by IQSS][].

You can contribute in one or more of the following ways:

- Update your installation's information on the [crowdsourced spreadsheet][]
- Request that your installation info on the [spreadsheet maintained by IQSS][] be updated (include what's new or what's changed) by adding a new issue to our [github issue][]j or by leaving a comment on the [spreadsheet maintained by IQSS][].
- If you have made (requested) changes to either of the info files, you can update the map by running the map update script (see **Requirements** below).
   - If you don't want to run the update script, create another [github issue][] to ask someoneelse to update the map.


## Updating the Map


### Requirements
*python 3* OR *docker*

- Fork this dataverse-installations repo to your github
- Clone your fork onto your local machine and follow the installation instructions to setup your environment
- Run the update program 

    `python3 update-data.py`

    OR

    `docker run --rm -v $PWD:/web -w /web -it python:3.7-alpine python3 update-data.py`

    This should update files in the "data" directory.

- Push the updated files to your github "fork"
- Create a pull request in github



### Coding style

`reformat-all.sh` is a script you can run from the root of the repo to format code but this is optional. We can always reformat code later.

## Security

If you would like to report a security issue, please email security@dataverse.org rather than creating an issue.

## Getting help

If you have questions or need help, please reach out at [chat.dataverse.org][] or the [dataverse-community Google Group][] or by creating an issue in the [issue tracker][].

[chat.dataverse.org]: http://chat.dataverse.org
[dataverse-community Google Group]: https://groups.google.com/group/dataverse-community
[issue tracker]: https://github.com/IQSS/dataverse-installations/issues
[Readme File]: README.md

[spreadsheet maintained by IQSS]:https://docs.google.com/spreadsheets/d/1l2R9D1FQy88qVzg2bI6L1LgplmM2l7pnMI80jdiz4fk/edit?usp=sharing
[crowdsourced spreadsheet]: https://docs.google.com/spreadsheets/d/1bfsw7gnHlHerLXuk7YprUT68liHfcaMxs1rFciA-mEo/edit#gid=0
[github issue]: https://github.com/IQSS/dataverse-installations/issues/new
