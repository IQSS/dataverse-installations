from django.contrib import admin
from dv_apps.guestbook.models import GuestBook, GuestBookResponse

class GuestBookAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('id',  'dataverse', 'name')
    readonly_fields = ('createtime',)
admin.site.register(GuestBook, GuestBookAdmin)

class GuestBookResponseAdmin(admin.ModelAdmin ):
    save_on_top = True
    list_display = ('id', 'downloadtype', 'responsetime', 'datafile' )#'guestbook', 'responsetime')
    readonly_fields = ('responsetime',)
admin.site.register(GuestBookResponse, GuestBookResponseAdmin)
