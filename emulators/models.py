from django.db import models
from django.urls import reverse
from consoles.models import Console

# Create your models here.
class Emulator(models.Model):
    name = models.CharField(max_length=100)
    console = models.ForeignKey(to=Console, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('emulators')
