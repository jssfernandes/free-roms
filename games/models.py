from django.db import models
from django.urls import reverse
from consoles.models import Console
# from files.models import Files

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=120)
    # source = models.ManyToManyField(Files)
    # console = models.ManyToManyField(Console, related_name='consoles')
    # console = models.ForeignKey(to=Console, related_name='consoles', null=False, blank=False, on_delete=models.PROTECT)
    console = models.ForeignKey(to=Console, on_delete=models.CASCADE)
    # console = models.ForeignKey(Console, related_name='console', null=True, blank=True, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games')
