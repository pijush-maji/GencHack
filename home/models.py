from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class Files(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.PROTECT)
    title=models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.title
