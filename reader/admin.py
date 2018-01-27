from django.contrib import admin

from .models import Manga, Chapter

# Register your models here.

class MangaAdmin(admin.ModelAdmin):
  list_display = ('title', 'status', 'display_method')
  
class ChapterAdmin(admin.ModelAdmin):
  list_display = ('getDisplay', 'title', 'upload_date', 'num_pages', 'visible')

admin.site.register(Manga, MangaAdmin)
admin.site.register(Chapter, ChapterAdmin)
