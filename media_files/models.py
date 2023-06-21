from django.db import models
from django.urls import reverse
from consoles.models import Console
from emulators.models import Emulator
from games.models import Game
# import os
# from django.core.files import File
# from urllib.request import urlopen
# from tempfile import NamedTemporaryFile

# Create your models here.
class MediaFile(models.Model):
    image_file = models.ImageField(upload_to='images/others', blank=True, null=True,)
    cover = models.BooleanField()
    photo = models.BooleanField()
    video = models.BooleanField()
    source_video = models.TextField(null=True, blank=True)
    console = models.ForeignKey(Console, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)
    emulator = models.ForeignKey(Emulator, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)

    # console = models.ForeignKey(Console, related_name='consoles', null=True, blank=True, on_delete=models.CASCADE)
    # emulator = models.ForeignKey(Emulator, related_name='emulators', null=True, blank=True, on_delete=models.CASCADE)
    # game = models.ForeignKey(Game, related_name='games', null=True, blank=True, on_delete=models.CASCADE)

    # consoles = models.ForeignKey(Console, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)
    # emulators = models.ForeignKey(Emulator, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)
    # games = models.ForeignKey(Game, related_name='mediafiles', null=True, blank=True, on_delete=models.CASCADE)
    # consoles = models.ManyToManyField(Console, related_name='mediafiles', blank=True)
    # emulators = models.ManyToManyField(Emulator, related_name='mediafiles', blank=True)
    # games = models.ManyToManyField(Game, related_name='mediafiles', blank=True)
    # def get_consoles(self, obj):
    #     return "\n".join([p.console for p in obj.consoles.all()])
    # def get_emulators(self, obj):
    #     return "\n".join([p.emulator for p in obj.emulators.all()])
    # def get_games(self, obj):
    #     return "\n".join([p.game for p in obj.games.all()])

    # def __str__(self):
    #     return self.id

    def get_absolute_url(self):
        return reverse('media-files')

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'image_file' and self.console is not None:
                field.upload_to = 'images/consoles/%s' % self.console.short_name
            if field.name == 'image_file' and self.emulator is not None:
                field.upload_to = 'images/emulators/%s' % self.emulator.short_name
            if field.name == 'image_file' and self.game is not None:
                field.upload_to = 'images/games/%s' % self.game.short_name
        super(MediaFile, self).save()

    class Meta:
        ordering = ['id']

    def __str__(self):
        # return self.image_file
        return self.game
