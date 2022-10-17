from django.db import models
from django.contrib.auth.models import User
from church.models import Church

class HeadUserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    church = models.ForeignKey(Church, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    foto = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    video = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
