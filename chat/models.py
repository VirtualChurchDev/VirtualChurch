from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=2000)
    
    class Meta:
        verbose_name_plural = 'rooms'
    
    def __str__(self):
        return self.name
    
    def get_text(self):
        return self.text
    
    def set_text(self, text):
        self.text = text
        return
