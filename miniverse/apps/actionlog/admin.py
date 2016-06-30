from django.contrib import admin

from .models import ActionLogRecord

class ActionLogRecordAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'useridentifier', 'actionresult', 'actiontype', 'actionsubtype', 'starttime', 'endtime')
    list_filter= ( 'actiontype', 'actionsubtype', 'useridentifier')
admin.site.register(ActionLogRecord, ActionLogRecordAdmin)

"""
id = models.CharField(primary_key=True, max_length=36)
actionresult = models.CharField(max_length=255, blank=True, null=True)
actionsubtype = models.CharField(max_length=255, blank=True, null=True)
actiontype = models.CharField(max_length=255, blank=True, null=True)
endtime = models.DateTimeField(blank=True, null=True)
info = models.CharField(max_length=1024, blank=True, null=True)
starttime = models.DateTimeField(blank=True, null=True)
useridentifier = models.CharField(max_length=255, blank=True, null=True)
"""
