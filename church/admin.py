from django.contrib import admin
from .models import News, Church

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted']


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
