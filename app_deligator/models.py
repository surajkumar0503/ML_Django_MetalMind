from django.db import models


# Create your models here.
class materials(models.Model):
    bauxite = models.IntegerField()
    aluminiumoxide = models.FloatField()
    carbon = models.FloatField()
    aluminiumfluoride = models.IntegerField()
    cryolite = models.IntegerField()
    electricalenergy = models.IntegerField()
    send_agent = models.BooleanField(default=False)
    progress_bar = models.BooleanField(default=False)
    aluminium = models.IntegerField(null=True)
    aluminium_predict = models.BooleanField(default=False)
    red_mud = models.FloatField(null=True)
    residue = models.BooleanField(default=False)
    scrap_send = models.BooleanField(default=False)
