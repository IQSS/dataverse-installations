from django.contrib import admin

from .models import Installation
from .models import Institution

# Register your models here.

admin.site.register(Installation)
admin.site.register(Institution)
