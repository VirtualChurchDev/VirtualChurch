from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2000)
    posted = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'News'
    
    
    def __str__(self):
        return self.title
