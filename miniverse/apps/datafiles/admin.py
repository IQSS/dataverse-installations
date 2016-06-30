from django.contrib import admin

from .models import Datafile


class DatafileAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id',  'filesystemname', 'filesize', 'contenttype', 'ingeststatus', 'restricted')
    list_filter= ( 'ingeststatus', 'restricted', 'contenttype', )
admin.site.register(Datafile, DatafileAdmin)
