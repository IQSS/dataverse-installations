from dv_apps.datasets.models import *
from dv_apps.datasets.models import Datafile

# extension
# time range
# harvested/non-harvest

Select count(*) from datafile where filesize is null;
Select count(*) from datafile where filesize = 0;

select count(*) from dataset where;

select count(df.id) from datafile df, dvobject dv
where df.filesize is null
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is not null);

 where datafile
select id from dataset where harvestingclient_id is null;


Fizesize is null

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
