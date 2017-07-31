(a bit incomplete 7.31.2017)

### Load/keep test fixtures

```
python manage.py test --keepdb
python manage.py loaddata --database=dataverse dv_apps/metrics/fixtures/test_yyy_mmdd.json
```

### Run migrate scripts on test db

- example from 4.7.x upgrade

```sql
# run sql scripts
```

- adjust models appropriately

### Dump fixtures with adjusted data

```
python manage.py dumpdata --database=dataverse --indent=4 dvobjects.dvobject dataverses.dataverse dataverses.dataverserole dataverses.dataversetheme dataverses.dataversecontact dataverses.template datasets.dataset datasets.datasetversion datafiles.datafile datafiles.filemetadata dataverse_auth.authenticateduser dataverse_auth.apitoken guestbook.guestbook guestbook.guestbookresponse > dv_apps/metrics/fixtures/test_2017_0731.json
```
