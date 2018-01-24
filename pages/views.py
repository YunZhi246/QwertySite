from django.shortcuts import render
from reader.models import Chapter
from django.core.mail import EmailMultiAlternatives
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
  htmlContent = '<b>Name:</b> ' + request.POST['name'] + '<br/><br/><b>Email:</b> ' + request.POST['email']
  htmlContent = htmlContent + '<br/><br/><b>Comment:</b> ' + request.POST['comment']  
  subject = 'New Comment from ' +  request.POST['name']
  replyToEmail = request.POST['email']
  email = EmailMultiAlternatives(
             subject,
             emailContent,
             'from@example.com',
             ['to@example.com'],
             reply_to=[replyToEmail],
           )  
  email.attach_alternative(htmlContent, "text/html")
  email.send(fail_silently=False)
  return HttpResponseRedirect(reverse('pages:contactUs', args=("sent", )))