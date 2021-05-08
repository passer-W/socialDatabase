from django.db import models

# Create your models here.

class Info(models.Model):
    name = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    identity = models.CharField(max_length=50)
    xh = models.CharField(max_length=50)
    mm = models.CharField(max_length=50)
    sfzh = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
