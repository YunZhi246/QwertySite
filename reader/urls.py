# reader.urls.py

from django.urls import path

from . import views

app_name = 'reader'
urlpatterns = [
    path('', views.index, name='index'),
    path('<mangaSeries>', views.mangaDetail, name='mangaDetail'),
    path('<mangaSeries>/<int:chapterId>/readChapter/', views.readChapter, name='readChapter'),
    path('<mangaSeries>/<int:chapterId>', views.stripReader, name='stripReader'),
    path('<mangaSeries>/<int:chapterId>/<int:pageNum>', views.pageReader, name='pageReader'),
    path('<mangaSeries>/jump/<display>', views.jumpChapter, name='jumpChapter'),
    path('<mangaSeries>/<int:chapterId>/jump', views.jumpPage, name='jumpPage'),
    path('upload/', views.upload, name='upload'),
    path('upload/<chapterUploaded>', views.upload, name='upload'),
    path('upload/submit_chapter/', views.submitChapter, name='submitChapter'),

]
