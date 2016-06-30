from django.contrib import admin

from .models import MetadataBlock, DatasetFieldType, ControlledVocabularyValue,\
    DatasetField, DatasetFieldCompoundValue, DatasetFieldValue, DatasetFieldControlledVocabularyValue
from .forms import ControlledVocabularyInlineForm


class MetadataBlockAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('displayname', 'name', 'owner',)
    #readonly_fields = ('dataset',)# 'identifier_string' )
    #list_filter= ('versionstate',)
    list_display_links = ('displayname', 'name')

admin.site.register(MetadataBlock, MetadataBlockAdmin)

class DatasetfieldControlledVocabularyValueAdmin(admin.ModelAdmin):
    save_on_top = True
    #search_fields = ('controlledvocabularyvalues__strvalue',)
    #list_display = ('datasetfield', 'controlledvocabularyvalues')
admin.site.register(DatasetFieldControlledVocabularyValue, DatasetfieldControlledVocabularyValueAdmin)


class ControlledVocabularyValueInline(admin.TabularInline):
    model = ControlledVocabularyValue
    form = ControlledVocabularyInlineForm
    fields = ('strvalue', 'displayorder', 'identifier')
    extra = 0


class DatasetFieldTypeAdmin(admin.ModelAdmin ):
    inlines = [ControlledVocabularyValueInline]
    save_on_top = True
    list_display = ('name', 'required', 'description', 'metadatablock', 'allowcontrolledvocabulary',   'fieldtype')
    #readonly_fields = ('dataset',)# 'identifier_string' )
    list_filter= ('required', 'allowcontrolledvocabulary', 'metadatablock', 'fieldtype')
    list_display_links = ('name', 'description')
    search_fields = ('name', 'description', )
admin.site.register(DatasetFieldType, DatasetFieldTypeAdmin)



class ControlledVocabularyValueAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('strvalue', 'datasetfieldtype', 'identifier', 'displayorder',)
    #readonly_fields = ('dataset',)# 'identifier_string' )
    list_filter= ('datasetfieldtype', )
    list_display_links = ('strvalue', 'datasetfieldtype')
admin.site.register(ControlledVocabularyValue, ControlledVocabularyValueAdmin)



class DatasetFieldAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('datasetfieldtype',  'template',)
    #'parentdatasetfieldcompoundvalue', 'datasetversion',
    list_display_links = ('datasetfieldtype', )
    list_filter= ('datasetversion',)# 'parentdatasetfieldcompoundvalue')

admin.site.register(DatasetField, DatasetFieldAdmin)


class DatasetFieldValueAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('value', 'displayorder',)
    #list_filter= ('datasetfield',)
    search_fields = ('value',)
admin.site.register(DatasetFieldValue, DatasetFieldValueAdmin)



class DatasetFieldCompoundValueAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'displayorder', 'parentdatasetfield')
admin.site.register(DatasetFieldCompoundValue, DatasetFieldCompoundValueAdmin)
