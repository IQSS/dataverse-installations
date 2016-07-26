from django.contrib import admin

from .models import DvObject


class DvObjectAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('id',  'dtype', 'owner', 'createdate', 'modificationtime', 'publicationdate', 'indextime')
    readonly_fields = ('createdate', 'modificationtime', )
    list_filter= ('dtype', )

admin.site.register(DvObject, DvObjectAdmin)
