
from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile, FileMetadata
from django.db.models import Q

Datafile.objects.filter(filesize=0).count()
Datafile.objects.filter(filesize__isnull=True).count()

Dataset.objects.filter(harvestingclient__isnull=True).values_list('dvobject__id', flat=True)

Dataset.objects.filter(harvestingclient__isnull=True).count()

ds_ids_harvested = Dataset.objects.filter(harvestingclient__isnull=True).values_list('dvobject__id', flat=False)

# Non-harvested datasets
Dataset.objects.filter(harvestingclient__isnull=True).count()

# count of harvested datasets
num_harvested_datasets = Dataset.objects.filter(harvestingclient__isnull=False).count()


# Dataset ids - Harvested
ds_ids_harvested = Dataset.objects.filter(harvestingclient__isnull=False\
                                ).values_list('dvobject__id', flat=True)

# Dataset ids - non-Harvested
ds_ids_non_harvested = Dataset.objects.filter(harvestingclient__isnull=True\
                                ).values_list('dvobject__id', flat=True)

# File count - harvested with size 0 or null
Datafile.objects.filter(Q(filesize=0) | Q(filesize__isnull=True),
                ).filter(dvobject__owner_id__in=ds_ids_harvested).count()

# File count - non-harvested with size 0 or null
Datafile.objects.filter(Q(filesize=0) | Q(filesize__isnull=True),
                ).filter(dvobject__owner_id__in=ds_ids_non_harvested).count()

Datafile.objects.filter(Q(filesize=0) | Q(filesize__isnull=True),
                ).filter(dvobject__owner_id__in=Dataset.objects.filter(harvestingclient__isnull=True\
                                                ).values_list('dvobject__id', flat=True)).count()

# Harvested datafiles


Datafile.objects.filter(dvobject__owner__harvestingclient__isnull=True).count()
Datafile.objects.filter(dvobject__owner__harvestingclient__isnull=False).count()

"""Fizesize is null

All: 31,177 (1c)
Local: 125  (1b)
Harvested: 31,052 (1c)

---

Fizesize is 0

All: 108,156 (2a)
Local: 493 (2b)
Harvested: 107,663 (2c)

---

(1a) ```Select count(*) from datafile where filesize is null;```

(1b) ```select count(df.id) from datafile df, dvobject dv
where df.filesize is null
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is not null);```

(1c) ```select count(df.id) from datafile df, dvobject dv
where df.filesize is null
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is null);```

---

(2a) ```Select count(*) from datafile where filesize = 0;```

(2b) ```select count(df.id) from datafile df, dvobject dv
where df.filesize = 0
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is null);```

(2c) ```select count(df.id) from datafile df, dvobject dv
where df.filesize = 0
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is not null);```
"""
