from django.contrib import admin
from .models import Person, Category, Comment
from django.db import models

admin.site.register(Person)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment)