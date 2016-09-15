"""
Output SQL fixes for each content type
"""

class CommentBuilder(object):

    def __init__(self, cnt, filetype_name, file_ext, new_type, ref_url):
        self.cnt = cnt
        self.name = filetype_name
        self.file_ext = file_ext
        self.new_type = new_type
        self.ref_url = ref_url

    def get_checklist(self):
        return """- [ ] %s. Fix ```%s``` files
    - Change extension ```%s``` to contenttype ```%s```""" %\
        (self.cnt, self.name, self.file_ext, self.new_type)

    def get_instructions(self):

        return """
# (%s) Fix ```%s``` files
  - Change extension ```%s``` to contenttype ```%s```:
  - reference: %s

## A - Run subquery count
%s

## B - Run update query
%s
## Sanity

  - Counts in **A** and **B** should match.

        """ % (self.cnt, self.name, self.file_ext, self.new_type, self.ref_url,\
        self.get_query_01_count(), self.get_query_02_change())

    def get_query_01_count(self):

        return """
```sql
SELECT count(distinct(df.id))
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%%%s'
AND df.contenttype = 'application/octet-stream';
```""" % (self.file_ext)

    def get_query_02_change(self):

        return """
```sql
BEGIN;
update datafile set contenttype='%s' where id in (SELECT distinct(df.id)
FROM datafile df,  filemetadata fm
WHERE fm.datafile_id = df.id
AND fm.label LIKE '%%%s'
AND df.contenttype = 'application/octet-stream');

/**
Check if it works!  e.g. File count matches!
*/
COMMIT;
```
""" % (self.new_type, self.file_ext)


def run_comment_builder():
    """
    Reference: http://www.iana.org/assignments/media-types/media-types.xhtml
    """
    l = [("DICOM (Digital Imaging and Communications in Medicine)", ".dcm", "image/dicom-rle", 5156, "http://www.iana.org/assignments/media-types/image/dicom-rle"),

    ("Nesstar files (Norwegian Center for Data Research)", ".NSDstat", "application/x-nsdstat", 7429, "http://www.nesstar.com/support/faq.html#pub.cubes_old_nsdstat"),

    (".xz format for compressed streams", ".xz", "application/x-xz", 12423,
    "http://tukaani.org/xz/xz-file-format.txt"),

    ("MS Word (.docx)", ".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 3646, "http://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc"),

    ("MS Word (.doc)", ".doc", "application/msword", 1534,
    "http://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc"),

    ("PDF files(.pdf)", ".pdf", "application/pdf", 1227, "http://stackoverflow.com/questions/312230/proper-mime-media-type-for-pdf-files"),
     ]

    print '\n'.join(['  - **%s**: %s files' % (x[1], x[3]) for x in l])
    print sum([x[3] for x in l])


    cnt = 0
    for info in l:
        cnt += 1
        cm = CommentBuilder(cnt, info[0], info[1], info[2], info[4])
        #print cm.get_instructions()
        print cm.get_checklist()

if __name__ == '__main__':
    run_comment_builder()
