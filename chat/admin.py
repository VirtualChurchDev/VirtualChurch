from django.contrib import admin
from .models import Room, Report

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'user']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['client', 'head']
