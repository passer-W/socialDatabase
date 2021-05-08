from django.db import models

# Create your models here.

class Invitee(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    isActive = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)