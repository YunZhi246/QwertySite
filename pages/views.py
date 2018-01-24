from django.shortcuts import render
from reader.models import Chapter
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.

def home(request):
  chapterList = Chapter.objects.order_by('-upload_date')[:6]
  context = {
    'chapter_list': chapterList,
  }
  return render(request, 'pages/home.html', context)

def aboutUs(request):
  return render(request, 'pages/about_us.html')

def recruit(request):
  return render(request, 'pages/recruitment.html')

def contactUs(request, msg=False):
  context = {}
  if msg == "sent":
    context = {
      'msg': 'Comment sent!',
    }
  return render(request, 'pages/contact_us.html', context)

def contactForm(request):
  emailContent = 'Name: \n' + request.POST['name'] + '\n\nEmail: \n' + request.POST['email']
  emailContent = emailContent + '\n\nComment: \n' + request.POST['comment']
  subject = 'New Comment from ' +  request.POST['name']
  result = send_mail(
             subject,
             emailContent,
             'from@example.com',
             ['j.lcrystal1234@yahoo.ca'],
             fail_silently=False,
           )  
  if result == 1:
    result = "sent"
  else:
    result = ""
  return HttpResponseRedirect(reverse('pages:contactUs', args=(result, )))