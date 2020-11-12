from django.contrib import admin
from .models import Veteran, Remembrance
from .forms import BioFormAdmin

# Register your models here.


class BioAdmin(admin.ModelAdmin):
    form = BioFormAdmin
    list_display = ("__str__", "approved")
    list_filter = ["approved"]

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.5.1/tinymce.min.js',
            'js/admin/custom.js',
        )


class StatusFilter(admin.ModelAdmin):
    list_display = ("__str__", "approved")
    list_filter = ["approved"]


admin.site.register(Veteran, BioAdmin)
admin.site.register(Remembrance, StatusFilter)
