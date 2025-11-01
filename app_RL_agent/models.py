from django.db import models


# Create your models here.
class rlAgentRegistration(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    contact = models.PositiveBigIntegerField()
    date_of_birth = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    