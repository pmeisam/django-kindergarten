from django.db import models
from django.urls import reverse
# Create your models here.
class Kid(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField(max_length=250)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"kid_id": self.id})