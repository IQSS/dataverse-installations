from django.contrib import admin

# Register your models here.
from dv_apps.dataset_docs.models import DatasetDoc


class DatasetDocAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('name', 'semantic_version', 'dataset_version_id', 'created',  'modified', )
    readonly_fields = ('created', 'modified')

admin.site.register(DatasetDoc, DatasetDocAdmin)
