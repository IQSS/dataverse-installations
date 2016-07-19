from django.db import models

class ActionLogRecord(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    actionresult = models.CharField(max_length=255, blank=True, null=True)
    actionsubtype = models.CharField(max_length=255, blank=True, null=True)
    actiontype = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    info = models.CharField(max_length=1024, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    useridentifier = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.actiontype, self.useridentifier)

    class Meta:
        ordering = ('-starttime',)
        managed = False
        db_table = 'actionlogrecord'
