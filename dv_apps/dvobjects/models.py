from django.db import models
#from django.contrib.auth.models import User

DTYPE_DATAVERSE = 'Dataverse'
DTYPE_DATASET = 'Dataset'
DTYPE_DATAFILE = 'DataFile'

DTYPES = (DTYPE_DATAVERSE, DTYPE_DATASET, DTYPE_DATAFILE)
DTYPE_CHOICES = [ (d, d) for d in DTYPES]


class DvObject(models.Model):

    dtype = models.CharField(max_length=31, choices=DTYPE_CHOICES)

    createdate = models.DateTimeField(auto_now_add=True)
    modificationtime = models.DateTimeField(auto_now=True)

    indextime = models.DateTimeField(blank=True, null=True)
    permissionindextime = models.DateTimeField(blank=True, null=True)
    permissionmodificationtime = models.DateTimeField(blank=True, null=True)

    publicationdate = models.DateTimeField(blank=True, null=True)

    owner = models.ForeignKey('self', blank=True, null=True)


    #releaseuser = models.ForeignKey(User, blank=True, null=True)
    #creator = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return '%s' % self.id
        #'%s (%s)' % (str(self.id).zfill(9), self.dtype)

    class Meta:
        managed = False
        db_table = 'dvobject'
