from django.contrib import admin

# Register your models here.
from .models import Installation, Institution

class InstallationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'full_name', 'logo', 'view_logo_100',  'url', 'marker', 'view_marker', 'version', 'description']
    readonly_fields = ('view_logo', 'view_logo_100', 'view_marker')
    list_editable = ['name']
    search_fields = ['name', 'full_name', 'description']

"""
lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
lng = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
logo = models.ImageField(upload_to='logos/', null=True, blank=True)
marker = models.ImageField(upload_to='logos/', null=True, blank=True)
description = models.TextField(null=True, blank=True)
url = models.TextField(null=True, blank=True)
version = models.CharField(max_length=6, unique=False, null=True, blank=True)
"""

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'host']
    search_fields = ['name']
    list_filter = ['host']

admin.site.register(Installation, InstallationAdmin)
admin.site.register(Institution, InstitutionAdmin)
