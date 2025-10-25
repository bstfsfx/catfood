from django.contrib import admin
from .models import Food, Review

class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Food, FoodAdmin)
admin.site.register(Review)