# reader.urls.py

from django.urls import path

from . import views

app_name = 'reader'
urlpatterns = [
  path('', views.index, name='index'),
  path('<mangaSeries>', views.mangaDetail, name='mangaDetail'),
  path('<mangaSeries>/<int:chapterId>', views.stripReader, name='stripReader'),  
  path('upload/', views.upload, name='upload'),
  path('upload/<chapterUploaded>', views.upload, name='upload'),
  path('upload/submit_chapter/', views.submitChapter, name='submitChapter'),

]