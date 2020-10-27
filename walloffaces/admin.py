from django.contrib import admin
from .models import Veteran, Remembrance
# Register your models here.


class StatusFilter(admin.ModelAdmin):
    list_display = ("__str__", "approved")
    list_filter = ["approved"]


admin.site.register(Veteran, StatusFilter)
admin.site.register(Remembrance, StatusFilter)
