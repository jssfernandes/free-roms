from django.db import models
from django.urls import reverse
# from media_files.models import MediaFile

# Create your models here.
class Console(models.Model):
    # id_personalizado = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    # manufacturer = models.CharField(max_length=100)
    manufacturer = models.ForeignKey('Manufacturer', null=False, blank=False, on_delete=models.PROTECT)
    # media_files = models.ForeignKey(MediaFile, null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('consoles')

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    founded = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturers')