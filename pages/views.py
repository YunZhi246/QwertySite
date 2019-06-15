from django.shortcuts import render
from reader.models import Chapter
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import BlogPost


# Create your views here.

def home(request):
    chapterList = Chapter.objects.filter(visible=True).order_by('-upload_date')[:6]
    pinnedPost = BlogPost.objects.filter(pinned=True).order_by('-created_date')[:]
    blogPost = BlogPost.objects.filter(pinned=False).order_by('-created_date')[:]
    context = {
        'chapter_list': chapterList,
    }
    if len(pinnedPost) != 0:
        context['pinned_list'] = pinnedPost
    if len(blogPost) != 0:
        context['blog_list'] = blogPost
    return render(request, 'pages/home.html', context)


def aboutUs(request):
    return render(request, 'pages/about_us.html')


def recruit(request, msg=False):
    context = {}
    if msg == "sent":
        context = {
            'msg': 'Application sent!',
        }
    return render(request, 'pages/recruitment.html', context)


def contactUs(request, msg=False):
    context = {}
    if msg == "sent":
        context = {
            'msg': 'Comment sent!',
        }
    return render(request, 'pages/contact_us.html', context)


def contactForm(request):
    with open('etc/email.txt') as f:
        fromEmail = f.readline().strip()
        toEmail = f.readline().strip()
    emailContent = 'Name: \n' + request.POST['name'] + '\n\nEmail: \n' + request.POST['email']
    emailContent = emailContent + '\n\nComment: \n' + request.POST['comment']
    htmlContent = '<b>Name:</b> ' + request.POST['name'] + '<br/><br/><b>Email:</b> ' + request.POST['email']
    htmlContent = htmlContent + '<br/><br/><b>Comment:</b> ' + request.POST['comment']
    subject = 'New Comment from ' + request.POST['name']
    replyToEmail = request.POST['email']
    email = EmailMultiAlternatives(
        subject,
        emailContent,
        fromEmail,
        [toEmail],
        reply_to=[replyToEmail],
    )
    email.attach_alternative(htmlContent, "text/html")
    email.send(fail_silently=False)
    return HttpResponseRedirect(reverse('pages:contactUs', args=("sent",)))


def recruitForm(request):
    with open('etc/email.txt') as f:
        fromEmail = f.readline().strip()
        toEmail = f.readline().strip()
    nameEmail = 'Name: \n' + request.POST['name'] + '\n\nEmail: \n' + request.POST['email']
    posiExper = '\n\nDesired Position: \n' + request.POST[
        'position'] + '\n\nDo you have experience with the position you selected? \n' + request.POST['experience']
    groups = '\n\nAre you in any other groups? If yes, please list them below. If no, skip this question. \n' + \
             request.POST['groups']
    proj = '\n\nWhat project are you interested in working on? \n' + request.POST['projects']
    selfIntro = '\n\nTell us a bit about yourself. \n' + request.POST['selfintro']
    discov = '\n\nHow did you discover us? \n' + request.POST['discovery']
    reason = '\n\nWhy do you want to join our team? \n' + request.POST['reason']
    comment = '\n\nIs there anything else you want to tell us? Questions, comments, past experience, whether or not you are applying for another position.\n' + \
              request.POST['comment']
    emailContent = nameEmail + posiExper + proj + selfIntro + discov + reason + comment

    hnameEmail = '<b>Name:</b> ' + request.POST['name'] + '<br/><br/><b>Email:</b> ' + request.POST['email']
    hposiExper = '<br/><br/><b>Desired Position: </b>' + request.POST[
        'position'] + '<br/><br/><b>Do you have experience with the position you selected? </b>' + request.POST[
                     'experience']
    hgroups = '<br/><br/><b>Are you in any other groups? If yes, please list them below. If no, skip this question. </b>' + \
              request.POST['groups']
    hproj = '<br/><br/><b>What project are you interested in working on? </b>' + request.POST['projects']
    hselfIntro = '<br/><br/><b>Tell us a bit about yourself. </b>' + request.POST['selfintro']
    hdiscov = '<br/><br/><b>How did you discover us? </b>' + request.POST['discovery']
    hreason = '<br/><br/><b>Why do you want to join our team? </b>' + request.POST['reason']
    hcomment = '<br/><br/><b>Is there anything else you want to tell us? Questions, comments, past experience, whether or not you are applying for another position.</b>' + \
               request.POST['comment']
    htmlContent = hnameEmail + hposiExper + hgroups + hproj + hselfIntro + hdiscov + hreason + hcomment

    subject = 'New Application from ' + request.POST['name']
    replyToEmail = request.POST['email']
    email = EmailMultiAlternatives(
        subject,
        emailContent,
        fromEmail,
        [toEmail],
        reply_to=[replyToEmail],
    )
    email.attach_alternative(htmlContent, "text/html")
    email.send(fail_silently=False)
    return HttpResponseRedirect(reverse('pages:recruit', args=("sent",)))
