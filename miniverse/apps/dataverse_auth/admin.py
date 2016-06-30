from django.contrib import admin

from .models import ApiToken, AuthenticatedUser


class ApiTokenAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['tokenstring', 'authenticateduser__lastname', 'authenticateduser__firstname', 'authenticateduser__useridentifier']
    list_display = ('authenticateduser', 'tokenstring', 'disabled', 'expiretime', 'createtime')
    list_filter= ( 'disabled', )
admin.site.register(ApiToken, ApiTokenAdmin)

class AuthenticatedUserAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('useridentifier', 'email', 'lastname', 'firstname', 'affiliation')
    list_display = ('useridentifier', 'superuser', 'email', 'lastname', 'firstname', 'affiliation', 'modificationtime')
    list_filter= ( 'superuser', 'affiliation')
admin.site.register(AuthenticatedUser, AuthenticatedUserAdmin)
