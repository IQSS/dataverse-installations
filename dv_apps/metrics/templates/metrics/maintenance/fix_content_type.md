
# Fix ```{{ file_extension }}``` files with unkown content types
  - Change extension ```{{ file_extension }}``` to contenttype ```{{ new_content_type }}```:

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%{{ file_extension }}'
AND df.contenttype = '{{ new_content_type }}';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='%s' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%{{ file_extension }}'
AND df.contenttype = '{{ new_content_type }}');

/**
Check if it works!  e.g. Do file counts matches?
If not:  ROLLBACK;
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.
