from django.contrib import admin

from .models import Datafile, FileMetadata, DatafileTag, DatafileCategory,\
    FilemetadataDatafileCategory


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


class DatafileCategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('name', 'dataset')
admin.site.register(DatafileCategory, DatafileCategoryAdmin)


class DatafileTagAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('dtype', 'datafile')
admin.site.register(DatafileTag, DatafileTagAdmin)

class FilemetadataDatafileCategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('filemetadatas__label',)
    list_display = ('filecategories', 'filemetadatas')
admin.site.register(FilemetadataDatafileCategory, FilemetadataDatafileCategoryAdmin)
