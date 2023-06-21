from django.db import models
from games.models import Game
from emulators.models import Emulator

# Create your models here.
class File(models.Model):
    source = models.TextField()
    # game = models.ManyToManyField(Console)
    game = models.ForeignKey(to=Game, related_name='files', null=True, blank=True, on_delete=models.CASCADE)
    emulator = models.ForeignKey(to=Emulator, related_name='files', null=True, blank=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        return reverse('files')
