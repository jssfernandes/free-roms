from django.contrib import admin
from .models import Console, Manufacturer
from media_files.models import MediaFile

# Register your models here.
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manufacturer', 'short_name' )
    # list_editable = ('name',)
    list_display_links = ('id', 'name', 'short_name' )
    list_per_page = 10
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "media_files":
            kwargs["queryset"] = MediaFile.objects.filter(console=request.user)
        return super(ConsoleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'founded')
    # list_editable = ('name',)
    list_display_links = ('id', 'name', 'founded' )
    list_per_page = 10

admin.site.register(Console, ConsoleAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
