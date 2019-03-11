from django.db import models
# Create your models here.
class Kid(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField(max_length=250)