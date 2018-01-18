from django.shortcuts import render

# Create your views here.

def home(request):
#  mangaList = Manga.objects.order_by('title')[:]
#  context = {
#    'manga_list': mangaList,
#  }
  return render(request, 'pages/home.html')

def aboutUs(request):
  return render(request, 'pages/about_us.html')

def recruit(request):
  return render(request, 'pages/recruitment.html')

def contactUs(request):
  return render(request, 'pages/contact_us.html')