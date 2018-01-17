from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.db import models
from django.contrib.auth.decorators import permission_required

from .models import Manga, Chapter, Page

import os, errno, zipfile
import re

# Create your views here.

def index(request):
  mangaList = Manga.objects.order_by('title')[:]
  context = {
    'manga_list': mangaList,
  }
  return render(request, 'reader/index.html', context)

def mangaDetail(request, mangaSeries):
  try:
    manga = Manga.objects.get(storage_name=mangaSeries)
  except(KeyError, Choice.DoesNotExist):
    render(request, 'reader/index.html')
  chapterList = manga.chapter_set.order_by('-sort_number')[:]
  context = {
    'manga': manga,
    'chapter_list': chapterList,
  }
  return render(request, 'reader/manga_details.html', context)  

def stripReader(request, mangaSeries, chapterId):
  try:
    manga = Manga.objects.get(storage_name=mangaSeries)
  except(KeyError, Choice.DoesNotExist):
    render(request, 'reader/index.html')
  try:
    chapter = Chapter.objects.get(pk=chapterId)
  except(KeyError, Choice.DoesNotExist):
    render(request, 'reader/{0}.html'.format(mangaSeries)) 
  
  chapterList = manga.chapter_set.order_by('sort_number')[:]
  prevId = 0
  nextId = 0
  chapLen = len(chapterList)
  for i in range(0, chapLen):
    if chapterList[i]==chapter:
      if(i!=chapLen-1):
        nextId = chapterList[i+1].id
      if(i!=0):
        prevId = chapterList[i-1].id
      break
  
  pageList = chapter.page_set.order_by('number')[:]
  pageUrls = []
  for page in pageList:
    strurl = str(page.image)
    pageUrls.append(strurl)
  
  context = {
    'manga': manga,
    'chapter': chapter,
    'prev_id': prevId,
    'next_id': nextId,
    'page_list': pageUrls,
  }
  return render(request, 'reader/stripReader.html', context)
  
@permission_required('add_chapter', login_url='accounts:login')
def upload(request, chapterUploaded=""): 
  mangaList = Manga.objects.order_by('title')[:]
  context = {
    'manga_list': mangaList,
    'chapter_uploaded': chapterUploaded,
  }
  return render(request, 'reader/upload.html', context)


def submitChapter(request):
  try:
    manga = Manga.objects.get(id=request.POST['manga'])
  except(KeyError, Choice.DoesNotExist):
    mangaList = Manga.objects.order_by('title')[:]    
    return render(request, 'reader/upload.html', {
      'manga_list': mangaList,
      'error_message':"You didn't select a manga choice.",
    })    
  chapNumber = request.POST['chap_number'].strip()
  volNumber = request.POST['vol_number'].strip()
  if(volNumber==""):
    volNumber = 0    
  if(chapNumber==""):
    return render(request, 'reader/upload.html', {
      'manga_list': mangaList,
      'error_message':"Please enter a chapter number!",
    })    
  sortNumber = int((float(volNumber)*1000000)+(float(chapNumber)*100))
  title = request.POST['title']
  owner = request.user
  upload_date = timezone.now()
  static = "reader\\static\\"
  path = "reader\\mangas\\"+manga.storage_name
  try:
    os.makedirs(static+path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      mangaList = Manga.objects.order_by('title')[:]    
      return render(request, 'reader/upload.html', {
        'manga_list': mangaList,
        'error_message':"Oops something went wrong, please try again.",
      })    
  chapterStorageName = str(sortNumber) + upload_date.strftime("%Y-%m-%d_%H-%M-%S_%f")
  path = path + "\\" + chapterStorageName
  try:
    os.makedirs(static+path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      mangaList = Manga.objects.order_by('title')[:]    
      return render(request, 'reader/upload.html', {
        'manga_list': mangaList,
        'error_message':"Oops something went wrong, please try again.",
      })    
                    
    
  myfile = request.FILES['chapter_file']
  fs = FileSystemStorage()
  filename = fs.save(myfile.name, myfile)
  uploaded_file_url = fs.url(filename)
    
  sortedList = []
  with zipfile.ZipFile(uploaded_file_url) as myzip:
    unsortedList = myzip.namelist()
    for name in unsortedList:
      if(re.match("^.*\.png$", name)!=None):
        sortedList.append(name)
      elif(re.match("^.*\.jpg$", name)!=None):
        sortedList.append(name)
    sortedList.sort()
    myzip.extractall(static+path, sortedList)
  
  chapter = Chapter(manga=manga,
                    chap_number=chapNumber, 
                    vol_number=volNumber, 
                    sort_number=sortNumber, 
                    title=title,
                    num_pages=len(sortedList),
                    owner=owner,
                    upload_date=upload_date,
                    storage_name=chapterStorageName,)
  chapter.save()
  
  for i in range (0, len(sortedList)):
    page = Page(chapter=chapter, number=i, image=path+"\\"+sortedList[i])
    page.save()
    
  os.remove(uploaded_file_url)
  return HttpResponseRedirect(reverse('reader:upload', args=(manga.title,)))
  
