from django.contrib import admin
from .models import MediaFile

# Register your models here.
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_file', 'cover', 'photo', 'video', 'console', 'emulator', 'game')
    # list_display = ('id', 'image_file', 'cover', 'photo', 'video', 'get_consoles', 'get_emulators', 'get_games')
    # list_editable = ('name',)
    list_display_links = ('id', 'image_file', 'cover', 'photo', 'video', 'console', 'emulator', 'game')
    # list_display_links = ('id', 'image_file', 'cover', 'photo', 'video', 'get_consoles', 'get_emulators', 'get_games')
    list_per_page = 10

admin.site.register(MediaFile, MediaFileAdmin)
