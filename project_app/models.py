from django.db import models

# Create your models here.
class Tables(models.Model):
    name = models.TextField()
    desc = models.TextField()