from django.db import models

# Create your models here.

class AnimeGlobal(models.Model):
    title           = models.CharField(max_length=250)
    directedBy      = models.CharField(max_length=250, null = True)
    producedBy      = models.CharField(max_length=250, null = True)
    writtenBy       = models.CharField(max_length=250, null = True)
    musicBy         = models.CharField(max_length=250, null = True)
    studio          = models.CharField(max_length=250, null = True)
    licensedBy      = models.CharField(max_length=250, null = True)
    originalNetwork = models.CharField(max_length=250, null = True)
    englishNetwork  = models.CharField(max_length=250, null = True)
    originalRun     = models.CharField(max_length=250, null = True)
    episodes        = models.IntegerField()

