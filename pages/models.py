from django.db import models
from django.contrib import auth, admin
from django.utils import timezone

# Create your models here.

class BlogPost(models.Model):
  title = models.CharField(max_length=200, blank=False)
  created_date = models.DateTimeField('date', editable=False, default=timezone.now)
  writer = models.ForeignKey(auth.models.User, on_delete=models.SET_NULL, null=True)
  RELEASES = 'RE'
  ANNOUCEMENTS = 'AN'
  category_choices = (
    (ANNOUCEMENTS, 'Annoucements'),
    (RELEASES, 'Releases'),
  )
  pinned = models.BooleanField(default=False)
  category = models.CharField(max_length=2, choices=category_choices, default=RELEASES)
  post = models.TextField(blank=False)
  def __str__(self):
    return self.title
  def getCategory(self):
    if self.category==BlogPost.RELEASES:
      return 'Releases'
    if self.category==BlogPost.ANNOUCEMENTS:
      return 'Annoucements'