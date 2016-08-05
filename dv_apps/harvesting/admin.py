from django.contrib import admin

from dv_apps.harvesting.models import HarvestingDataverseConfig

class HarvestingDataverseConfigAdmin(admin.ModelAdmin ):
    save_on_top = True
    search_fields = ('archivedescription',)
    list_display = ('id', 'archiveurl', 'harveststyle', 'harvesttype', 'archivedescription' )
    list_filter = ('harveststyle', 'harvesttype')
    readonlyfields = ('dataverse_name',)
    fields = ('archivedescription', 'archiveurl', 'harveststyle', 'harvesttype', 'harvestingset', 'harvestingurl', )
admin.site.register(HarvestingDataverseConfig, HarvestingDataverseConfigAdmin)
