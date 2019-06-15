from django.contrib import admin
from django.db import models
from .models import BlogPost


# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'post']}),
        ('Properties', {'fields': ['pinned', 'category']}),
    ]
    list_display = ('title', 'created_date', 'writer')

    def save_model(self, request, obj, form, change):
        obj.writer = request.user
        obj.save()


admin.site.register(BlogPost, BlogPostAdmin)
