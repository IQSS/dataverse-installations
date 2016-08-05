from django.contrib import admin

from .models import Datafile, FileMetadata


class DatafileAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('label', 'filesystemname')
    list_display = ('dvobject',  'filesystemname', 'filesize', 'contenttype', 'ingeststatus', 'restricted')
    list_filter= ( 'ingeststatus', 'restricted', 'contenttype', )
admin.site.register(Datafile, DatafileAdmin)


class FileMetadataAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('label', 'description')
    list_display = ('label', 'version', 'restricted', 'description', )
    list_filter= ('restricted',)
    fields = ( 'label', 'description', 'version', 'datafile',)# 'datasetversion')

admin.site.register(FileMetadata, FileMetadataAdmin)
