from django.shortcuts import render, get_object_or_404, Http404
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
    currentList = Manga.objects.all().filter(status=Manga.CURRENT).order_by('title')[:]
    completedList = Manga.objects.all().filter(status=Manga.COMPLETED).order_by('title')[:]
    hiatusList = Manga.objects.all().filter(status=Manga.HIATUS).order_by('title')[:]
    droppedList = Manga.objects.all().filter(status=Manga.DROPPED).order_by('title')[:]
    futureList = Manga.objects.all().filter(status=Manga.FUTURE).order_by('title')[:]
    litcList = Manga.objects.all().filter(status=Manga.LITC).order_by('title')[:]

    context = {}
    if len(currentList) != 0:
        context['current_list'] = currentList
    if len(completedList) != 0:
        context['completed_list'] = completedList
    if len(hiatusList) != 0:
        context['hiatus_list'] = hiatusList
    if len(droppedList) != 0:
        context['dropped_list'] = droppedList
    if len(futureList) != 0:
        context['future_list'] = futureList
    if len(litcList) != 0:
        context['litc_list'] = litcList

    return render(request, 'reader/index.html', context)


def mangaDetail(request, mangaSeries):
    try:
        manga = Manga.objects.get(storage_name=mangaSeries)
    except(KeyError, Manga.DoesNotExist):
        render(request, 'reader/index.html')
    chapterList = manga.chapter_set.filter(visible=True).order_by('-sort_number')[:]
    context = {
        'manga': manga,
        'chapter_list': chapterList,
    }
    return render(request, 'reader/manga_details.html', context)


def readChapter(request, mangaSeries, chapterId):
    try:
        manga = Manga.objects.get(storage_name=mangaSeries)
    except(KeyError, Manga.DoesNotExist):
        render(request, 'reader/index.html')
    try:
        chapter = Chapter.objects.get(pk=chapterId)
    except(KeyError, Chapter.DoesNotExist):
        raise Http404("Chapter does not exist")
    if manga.display_method == Manga.TRADITIONAL:
        return HttpResponseRedirect(reverse('reader:pageReader', args=(mangaSeries, chapterId, 1,)))
    elif manga.display_method == Manga.WEBTOON:
        return HttpResponseRedirect(reverse('reader:stripReader', args=(mangaSeries, chapterId,)))


def stripReader(request, mangaSeries, chapterId):
    try:
        manga = Manga.objects.get(storage_name=mangaSeries)
    except(KeyError, Manga.DoesNotExist):
        render(request, 'reader/index.html')
    try:
        chapter = Chapter.objects.get(pk=chapterId)
    except(KeyError, Chapter.DoesNotExist):
        raise Http404("Chapter does not exist")

    chapterList = manga.chapter_set.filter(visible=True).order_by('sort_number')[:]
    hasPrev = False
    hasNext = False
    prevId = 0
    nextId = 0
    chapLen = len(chapterList)
    for i in range(0, chapLen):
        if chapterList[i] == chapter:
            if (i != chapLen - 1):
                nextId = chapterList[i + 1].id
                hasNext = True
            if (i != 0):
                prevId = chapterList[i - 1].id
                hasPrev = True
            break

    pageList = chapter.page_set.order_by('number')[:]
    pageUrls = []
    for page in pageList:
        strurl = str(page.image)
        pageUrls.append(strurl)

    context = {
        'manga': manga,
        'chapter': chapter,
        'chapter_list': chapterList,
        'prev_id': prevId,
        'next_id': nextId,
        'page_list': pageUrls,
    }
    if hasPrev and (not hasNext):
        context = {
            'manga': manga,
            'chapter': chapter,
            'chapter_list': chapterList,
            'prev_id': prevId,
            'page_list': pageUrls,
        }
    elif hasNext and (not hasPrev):
        context = {
            'manga': manga,
            'chapter': chapter,
            'chapter_list': chapterList,
            'next_id': nextId,
            'page_list': pageUrls,
        }
    elif (not hasNext) and (not hasPrev):
        context = {
            'manga': manga,
            'chapter': chapter,
            'chapter_list': chapterList,
            'page_list': pageUrls,
        }

    return render(request, 'reader/stripReader.html', context)


def pageReader(request, mangaSeries, chapterId, pageNum):
    try:
        manga = Manga.objects.get(storage_name=mangaSeries)
    except(KeyError, Manga.DoesNotExist):
        render(request, 'reader/index.html')
    try:
        chapter = Chapter.objects.get(pk=chapterId)
    except(KeyError, Chapter.DoesNotExist):
        raise Http404("Chapter does not exist")
    try:
        page = chapter.page_set.get(number=pageNum)
    except(KeyError, Page.DoesNotExist):
        raise Http404("Page does not exist")

    pageUrl = str(page.image)
    pageList = [i for i in range(1, chapter.num_pages + 1)]

    hasNextPage = True
    hasPrevPage = True
    hasNextChap = False
    hasPrevChap = False
    prevPage = pageNum - 1
    nextPage = pageNum + 1
    prevChapId = 0
    nextChapId = 0
    prevChapNum = 0

    chapterList = manga.chapter_set.filter(visible=True).order_by('sort_number')[:]
    hasPrev = False
    hasNext = False
    chapLen = len(chapterList)
    for i in range(0, chapLen):
        if chapterList[i] == chapter:
            if (i != chapLen - 1):
                nextChapId = chapterList[i + 1].id
                hasNext = True
            if (i != 0):
                prevChapId = chapterList[i - 1].id
                hasPrev = True
                prevChapNum = chapterList[i - 1].num_pages
            break

    if pageNum == chapter.num_pages or pageNum == 1:
        if pageNum == chapter.num_pages:
            hasNextPage = False
            if hasNext:
                hasNextChap = True
        if pageNum == 1:
            hasPrevPage = False
            if hasPrev:
                hasPrevChap = True

    context = {
        'manga': manga,
        'chapter': chapter,
        'chapter_list': chapterList,
        'page_list': pageList,
        'page_num': pageNum,
        'page_url': pageUrl,
    }
    if hasNextPage:
        context['next_page'] = nextPage
    if hasPrevPage:
        context['prev_page'] = prev_page
    if hasNextChap:
        context['next_chap'] = nextChapId
    if hasPrevChap:
        context['prev_chap'] = prevChapId
        context['prev_chap_pages'] = prevChapNum
    return render(request, 'reader/pageReader.html', context)


def jumpPage(request, mangaSeries, chapterId):
    pageNum = request.POST['page']
    return HttpResponseRedirect(reverse('reader:pageReader', args=(mangaSeries, chapterId, pageNum,)))


def jumpChapter(request, mangaSeries, display):
    chapterId = request.POST['chapter']
    if display == 'webtoon':
        return HttpResponseRedirect(reverse('reader:stripReader', args=(mangaSeries, chapterId,)))
    elif display == 'pages':
        return HttpResponseRedirect(reverse('reader:pageReader', args=(mangaSeries, chapterId, 1)))
    else:
        raise Http404("URL does not exist")


@permission_required('reader.add_chapter', login_url='accounts:login')
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
    except(KeyError, Manga.DoesNotExist):
        mangaList = Manga.objects.order_by('title')[:]
        return render(request, 'reader/upload.html', {
            'manga_list': mangaList,
            'error_message': "You didn't select a manga choice.",
        })
    chapNumber = request.POST['chap_number'].strip()
    volNumber = request.POST['vol_number'].strip()
    if (volNumber == ""):
        volNumber = 0
    if (chapNumber == ""):
        mangaList = Manga.objects.order_by('title')[:]
        return render(request, 'reader/upload.html', {
            'manga_list': mangaList,
            'error_message': "Please enter a chapter number!",
        })
    sortNumber = int((float(volNumber) * 1000000) + (float(chapNumber) * 100))
    title = request.POST['title']
    owner = request.user
    upload_date = timezone.now()

    if os.name == 'nt':
        static = "reader\\static\\"
        path = "reader\\mangas\\" + manga.storage_name
    else:
        static = "static/"
        path = "reader/mangas/" + manga.storage_name

    try:
        os.makedirs(static + path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            mangaList = Manga.objects.order_by('title')[:]
            return render(request, 'reader/upload.html', {
                'manga_list': mangaList,
                'error_message': "Oops something went wrong, please try again.",
            })

    chapterStorageName = str(sortNumber) + upload_date.strftime("%Y-%m-%d_%H-%M-%S_%f")
    if os.name == 'nt':
        path = path + "\\" + chapterStorageName
    else:
        path = path + "/" + chapterStorageName

    try:
        os.makedirs(static + path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            mangaList = Manga.objects.order_by('title')[:]
            return render(request, 'reader/upload.html', {
                'manga_list': mangaList,
                'error_message': "Oops something went wrong, please try again.",
            })

    myfile = request.FILES['chapter_file']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)

    sortedList = []
    with zipfile.ZipFile(uploaded_file_url) as myzip:
        unsortedList = myzip.namelist()
        for name in unsortedList:
            if (re.match("^.*\.png$", name) != None):
                sortedList.append(name)
            elif (re.match("^.*\.jpg$", name) != None):
                sortedList.append(name)
        sortedList.sort()
        myzip.extractall(static + path, sortedList)

    chapter = Chapter(manga=manga,
                      chap_number=chapNumber,
                      vol_number=volNumber,
                      sort_number=sortNumber,
                      title=title,
                      num_pages=len(sortedList),
                      owner=owner,
                      upload_date=upload_date,
                      storage_name=chapterStorageName, )
    chapter.save()

    for i in range(1, len(sortedList) + 1):
        page = Page(chapter=chapter, number=i, image=path + "\\" + sortedList[i - 1])
        page.save()

    os.remove(uploaded_file_url)
    returnString = "{0} - {1}".format(manga.title, chapter)
    return HttpResponseRedirect(reverse('reader:upload', args=(returnString,)))
