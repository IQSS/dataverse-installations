  - **.dcm**: 5156 files
  - **.NSDstat**: 7429 files
  - **.xz**: 12423 files
  - **.docx**: 3646 files
  - **.doc**: 1534 files
  - **.pdf**: 1227 files
31415

# (1) Fix ```DICOM (Digital Imaging and Communications in Medicine)``` files
  - Change extension ```.dcm``` to contenttype ```image/dicom-rle```:
  - reference: http://www.iana.org/assignments/media-types/image/dicom-rle

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.dcm'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='image/dicom-rle' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.dcm'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        

# (2) Fix ```Nesstar files (Norwegian Center for Data Research)``` files
  - Change extension ```.NSDstat``` to contenttype ```application/x-nsdstat```:
  - reference: http://www.nesstar.com/support/faq.html#pub.cubes_old_nsdstat

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.NSDstat'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='application/x-nsdstat' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.NSDstat'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        

# (3) Fix ```.xz format for compressed streams``` files
  - Change extension ```.xz``` to contenttype ```application/x-xz```:
  - reference: http://tukaani.org/xz/xz-file-format.txt

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.xz'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='application/x-xz' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.xz'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        

# (4) Fix ```MS Word (.docx)``` files
  - Change extension ```.docx``` to contenttype ```application/vnd.openxmlformats-officedocument.wordprocessingml.document```:
  - reference: http://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.docx'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='application/vnd.openxmlformats-officedocument.wordprocessingml.document' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.docx'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        

# (5) Fix ```MS Word (.doc)``` files
  - Change extension ```.doc``` to contenttype ```application/msword```:
  - reference: http://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.doc'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='application/msword' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.doc'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        

# (6) Fix ```PDF files(.pdf)``` files
  - Change extension ```.pdf``` to contenttype ```application/pdf```:
  - reference: http://stackoverflow.com/questions/312230/proper-mime-media-type-for-pdf-files

## A - Run subquery count

```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.pdf'
AND df.contenttype = 'application/octet-stream';
```

## B - Run update query

```sql
BEGIN;
update datafile set contenttype='application/pdf' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%.pdf'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```

## Sanity

  - Counts in **A** and **B** should match.

        
