from django.contrib import admin
from .models import File

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'game', 'emulator' )
    # list_editable = ('name',)
    list_display_links = ('id', 'source', 'game', 'emulator' )
    list_per_page = 10

admin.site.register(File, FileAdmin)
