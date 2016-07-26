from django.contrib import admin

# Register your models here.
from .models import Installation, Institution

class InstallationAdmin(admin.ModelAdmin):
    list_display = ['name']
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'host']
    
admin.site.register(Installation, InstallationAdmin)
admin.site.register(Institution, InstitutionAdmin)