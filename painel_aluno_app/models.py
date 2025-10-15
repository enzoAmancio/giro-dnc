from django.db import models

# Create your models here.
class frequencia(models.Model):
    quantidade_falta = models.IntegerField(default=0)
 