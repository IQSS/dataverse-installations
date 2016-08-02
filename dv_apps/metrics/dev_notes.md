
# query for datasets created after 2015-01: 19.5k
#
SELECT to_char("dvobject"."createdate", 'YYYY-MM') AS "month_yyyy_dd", COUNT("dataset"."id") AS "cnt" FROM "dataset" INNER JOIN "dvobject" ON ("dataset"."id" = "dvobject"."id") WHERE "dvobject"."createdate" >= 2015-01-01 00:00:00+00:00 GROUP BY to_char("dvobject"."createdate", 'YYYY-MM') ORDER BY "month_yyyy_dd" ASC

# query for published datasets created after 2015-01: 17.8k
#
SELECT to_char("dvobject"."createdate", 'YYYY-MM') AS "month_yyyy_dd", COUNT("dataset"."id") AS "cnt" FROM "dataset" INNER JOIN "dvobject" ON ("dataset"."id" = "dvobject"."id") WHERE ("dvobject"."publicationdate" IS NOT NULL AND "dvobject"."createdate" >= 2015-01-01 00:00:00+00:00) GROUP BY to_char("dvobject"."createdate", 'YYYY-MM') ORDER BY "month_yyyy_dd" ASC

# query for unpublished datasets created after 2015-01: 1.7k
#
SELECT to_char("dvobject"."createdate", 'YYYY-MM') AS "month_yyyy_dd", COUNT("dataset"."id") AS "cnt" FROM "dataset" INNER JOIN "dvobject" ON ("dataset"."id" = "dvobject"."id") WHERE ("dvobject"."publicationdate" IS NULL AND "dvobject"."createdate" >= 2015-01-01 00:00:00+00:00) GROUP BY to_char("dvobject"."createdate", 'YYYY-MM') ORDER BY "month_yyyy_dd" ASC
