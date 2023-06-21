from django.contrib import admin
from .models import Emulator

# Register your models here.
class EmulatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'console', 'short_name', )
    # list_editable = ('name',)
    list_display_links = ('id', 'name', 'short_name', )
    list_per_page = 10

admin.site.register(Emulator, EmulatorAdmin)