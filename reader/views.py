from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

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
      'error_message':"You didn't select a choice.",
    })    
  chapNumber = request.POST['chap_number'].strip()
  volNumber = request.POST['vol_number'].strip()
  print(chapNumber)
  print(volNumber)
  sortNumber = int((float(volNumber)*1000000)+(float(chapNumber)*100))
  title = request.POST['title']
  upload_date = timezone.now()
  print(str(sortNumber))
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
                    upload_date=upload_date,
                    storage_name=chapterStorageName,)
  chapter.save()
  
  for i in range (0, len(sortedList)):
    page = Page(chapter=chapter, number=i, image=path+"\\"+sortedList[i])
    page.save()
    
  os.remove(uploaded_file_url)
  return HttpResponseRedirect(reverse('reader:upload', args=(manga.title,)))
  
