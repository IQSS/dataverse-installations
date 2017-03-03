from django.contrib import admin

from dv_apps.harvesting.models import HarvestingDataverseConfig,\
        HarvestingClient

class HarvestingDataverseConfigAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('archivedescription',)
    list_display = ('id', 'archiveurl',
                    'harveststyle', 'harvesttype',
                    'archivedescription')
    list_filter = ('harveststyle', 'harvesttype')
    readonlyfields = ('dataverse_name',)
    fields = ('archivedescription', 'archiveurl',
              'harveststyle', 'harvesttype',
              'harvestingset', 'harvestingurl')
admin.site.register(HarvestingDataverseConfig, HarvestingDataverseConfigAdmin)


class HarvestingClientAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name', 'archivedescription',)
    list_display = ('name', 'archivedescription',
                    'archiveurl', 'harveststyle', 'harvesttype')
admin.site.register(HarvestingClient, HarvestingClientAdmin)
