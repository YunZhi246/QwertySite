from django.db import models
from django.contrib import auth

# Create your models here.

class Manga(models.Model):
  title = models.CharField(max_length=200, blank=False, unique=True)
  alternative_titles = models.CharField(max_length=200, blank=True)
  author = models.CharField(max_length=50, blank=False)
  artist = models.CharField(max_length=50, blank=True)
  description = models.CharField(max_length=1000, blank=False)
  language = models.CharField(max_length=100, blank=True)
  genres = models.CharField(max_length=100, blank=True)
  joints = models.CharField(max_length=200, blank=True)
  pic_location = models.CharField(max_length=200, blank=False)
  storage_name = models.CharField(max_length=100, blank=False, unique=True)
  def __str__(self):
    return self.title

class Chapter(models.Model):
  manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
  chap_number = models.DecimalField(max_digits=5, decimal_places=2)
  vol_number = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  sort_number = models.PositiveIntegerField()
  title = models.CharField(max_length=200, blank=True)
  num_pages = models.PositiveSmallIntegerField()
  user = models.ForeignKey(auth.models.User, on_delete=models.SET_NULL, null=True)
  upload_date = models.DateTimeField('date uploaded')
  storage_name = models.CharField(max_length=100, blank=False)
  def __str__(self):
    displayName = " Chapter ".join(chap_number)
    if vol_number != 0:
      displayName = "Volume ".join(vol_number).join(displayName)
    if title != "":
      displayName = displayName.join(": ").join(title)
    return displayName
  
class Page(models.Model):
  chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)  
  number = models.PositiveSmallIntegerField()
  storage_name = models.CharField(max_length=100, blank=False)
  
  
  
  
  