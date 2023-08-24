from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_disabled=models.BooleanField(default=False)

    def __str__(self):
        return self.name