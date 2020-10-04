from django.db import models

# Create your models here.

class AnimePersonal(models.Model):
    title               = models.CharField(max_length=250)
    status              = models.CharField(max_length=20)
    finishedEpisodes    = models.IntegerField()
    endDate             = models.DateField()
    rating              = models.IntegerField()
    comment             = models.TextField(null=True)
    animeInfoPersonalId = models.IntegerField(null=True)
    animeGlobalId       = models.IntegerField(null=True)
    userId              = models.IntegerField()

class AnimeInfoPersonal(models.Model):
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
