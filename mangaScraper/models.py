from django.db import models

# Create your models here.

class MangaGlobal(models.Model):
    title            = models.CharField(max_length=250)
    writtenBy        = models.CharField(max_length=250, null = True)
    illustratedBy    = models.CharField(max_length=250, null = True)
    publishedBy      = models.CharField(max_length=250, null = True)
    englishPublisher = models.CharField(max_length=250, null = True)
    imprint          = models.CharField(max_length=250, null = True)
    magazine         = models.CharField(max_length=250, null = True)
    demographic      = models.CharField(max_length=250, null = True)
    originalRun      = models.CharField(max_length=250, null = True)
    volumes          = models.CharField(max_length=250, null = True)