from django.db import models

# Create your models here.

class MangaPersonal(models.Model):
    title               = models.CharField(max_length=250)
    status              = models.CharField(max_length=250)
    finishedVolumes     = models.IntegerField()
    endDate             = models.DateField()
    rating              = models.IntegerField()
    comment             = models.TextField(null=True)
    mangaInfoPersonalId = models.IntegerField(null=True)
    mangaGlobalId       = models.IntegerField(null=True)
    userId              = models.IntegerField()

class MangaInfoPersonal(models.Model):
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