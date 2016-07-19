python manage.py shell

from dv_apps.datasets.models import Dataset, DatasetVersion

l = DatasetVersion.objects.all()

for ds in l: print ds

for ds in l: print ds.id

"""
python manage.py dumpdata --indent=4 -e contenttypes -e auth.Permission -e dataverse_auth.ApiToken  > ../inspectdb_results/dump_2016-0628.json
python manage.py migrate
python manage.py loaddata ../inspectdb_results/dump_2016-0628.json
