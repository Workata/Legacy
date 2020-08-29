from django.db import models

# Create your models here.

class AnimeGlobal(models.Model):
    title = models.CharField(max_length=250)
    directedBy = models.CharField(max_length=250)
    producedBy = models.CharField(max_length=250)
    writtenBy = models.CharField(max_length=250)
    musicBy = models.CharField(max_length=250)
    studio = models.CharField(max_length=250)
    licensedBy = models.CharField(max_length=250)
    originalNetwork =  models.CharField(max_length=250)
    originalRun = models.CharField(max_length=250)
    episodes = models.IntegerField()
