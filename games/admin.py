from django.contrib import admin
from .models import Game

# Register your models here.
class GameAdmin(admin.ModelAdmin):
    # fields = ['name', 'console']
    # fields = ['console']
    # list_display = ('id', 'name', 'get_consoles', 'console_short_name', 'short_name')
    list_display = ('id', 'name', 'console', 'short_name')
    # list_editable = ('name',)
    list_display_links = ('id', 'name', 'short_name', )
    list_per_page = 10
    # def get_consoles(self, obj):
    #     return "\n".join([c.name for c in obj.console.all()])
    # def console_short_name(self, obj):
    #     return "\n".join([c.short_name for c in obj.console.all()])

admin.site.register(Game, GameAdmin)