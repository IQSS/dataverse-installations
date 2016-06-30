from django.contrib import admin

from .models import TermsOfUseAndAccess

class TermsOfUseAndAccessAdmin(admin.ModelAdmin ):
    #inlines = (DatasetInline,)
    search_fields = ('license', 'termsofaccess', 'termsofaccess', 'citationrequirements')
    save_on_top = True
    list_display = ('license', 'availabilitystatus',)
    list_filter = ('license', )
admin.site.register(TermsOfUseAndAccess, TermsOfUseAndAccessAdmin)

"""
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
"""
