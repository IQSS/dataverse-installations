from django.contrib import admin

from .models import Dataset, DatasetVersion

class DatasetAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('dvobject', 'identifier_string', 'protocol',  'authority', 'identifier', )
    readonly_fields = ('thumbnailfile', 'doiseparator', 'identifier_string' )
    list_filter= ('protocol',)
    list_display_links = ('dvobject', 'identifier_string')

    fieldsets = (
        ('Identifier', {
            'fields': ('identifier_string',
                       ('protocol', 'authority', 'identifier'),
                       'doiseparator')
        }),
        ('Timestamps', {
            'fields': ('globalidcreatetime',)
        }),
        ('File Access?', {
            'fields': ('fileaccessrequest',)
        }),
        ('Thumbnail File', {
            'fields': ('thumbnailfile',)
        }),
    )
admin.site.register(Dataset, DatasetAdmin)


class DatasetVersionAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('id', 'dataset', 'versionstate', 'versionnumber',  'minorversionnumber', )
    readonly_fields = ('dataset',)# 'identifier_string' )
    list_filter= ('versionstate',)
    list_display_links = ('id', 'dataset')

admin.site.register(DatasetVersion, DatasetVersionAdmin)
