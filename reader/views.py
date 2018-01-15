from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Manga

# Create your views here.

def index(request):
  mangaList = Manga.objects.order_by('-title')[:]
  pics = []
  context = {
    'manga_list': mangaList,
  }
  return render(request, 'reader/index.html', context)

def upload(request):
  return HttpResponse("Upload")
