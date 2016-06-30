from django.db import models


class TermsOfUseAndAccess(models.Model):
    termsofaccess = models.TextField(blank=True, null=True)
    termsofuse = models.TextField(blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)

    availabilitystatus = models.TextField(blank=True, null=True)
    citationrequirements = models.TextField(blank=True, null=True)

    conditions = models.TextField(blank=True, null=True)
    confidentialitydeclaration = models.TextField(blank=True, null=True)
    contactforaccess = models.TextField(blank=True, null=True)
    dataaccessplace = models.TextField(blank=True, null=True)
    depositorrequirements = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)

    fileaccessrequest = models.NullBooleanField()
    originalarchive = models.TextField(blank=True, null=True)
    restrictions = models.TextField(blank=True, null=True)
    sizeofcollection = models.TextField(blank=True, null=True)
    specialpermissions = models.TextField(blank=True, null=True)
    studycompletion = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.license:
            return self.license
        if self.termsofuse:
            return self.termsofuse
        else:
            return '(no terms of use specified)'

    class Meta:
        managed = False
        db_table = 'termsofuseandaccess'
