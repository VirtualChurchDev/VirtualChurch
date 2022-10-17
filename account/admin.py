from django.contrib import admin
from .models import HeadUserAccess

@admin.register(HeadUserAccess)
class HeadUserAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'name', 'church']
    prepopulated_fields = {'slug': ('name',)}
