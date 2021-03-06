from django.db import models
from django.contrib import auth


# Create your models here.

class Manga(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    alternative_titles = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=50, blank=False)
    artist = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    language = models.CharField(max_length=100, blank=True)
    genres = models.CharField(max_length=100, blank=True)
    COMPLETED = 'CP'
    CURRENT = 'CU'
    HIATUS = 'HT'
    DROPPED = 'DP'
    FUTURE = 'FT'
    LITC = 'LC'
    status_choices = (
        (COMPLETED, 'Completed'),
        (CURRENT, 'Current'),
        (HIATUS, 'Hiatus'),
        (DROPPED, 'Dropped'),
        (FUTURE, 'Future'),
        (LITC, "Lost in the Clouds"),
    )
    status = models.CharField(max_length=2, choices=status_choices, default=CURRENT)
    is_joint = models.BooleanField(default=False)
    joints = models.CharField(max_length=200, blank=True)
    TRADITIONAL = 0
    WEBTOON = 1
    display_choices = (
        (TRADITIONAL, 'Traditional (pages)'),
        (WEBTOON, 'Webtoon (strip view)'),
    )
    display_method = models.PositiveSmallIntegerField(choices=display_choices, default=WEBTOON)
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
    owner = models.ForeignKey(auth.models.User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField('date uploaded', editable=False)
    visible = models.BooleanField(default=True)
    storage_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        displayName = "Chapter {0}".format(
            str(round(float(self.chap_number), 2) if float(self.chap_number) % 1 else int(self.chap_number)))
        if self.vol_number != 0:
            displayName = "Volume {0} {1}".format(
                str(round(float(self.vol_number), 1) if float(self.vol_number) % 1 else int(self.vol_number)),
                displayName)
        if self.title != "":
            displayName = displayName + ": " + self.title
        return displayName

    def getDisplay(self):
        displayName = "Chapter {0}".format(
            str(round(float(self.chap_number), 1) if float(self.chap_number) % 1 else int(self.chap_number)))
        if self.vol_number != 0:
            displayName = "Volume {0} {1}".format(
                str(round(float(self.vol_number), 1) if float(self.vol_number) % 1 else int(self.vol_number)),
                displayName)
        displayName = self.manga.title + " " + displayName
        return displayName


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    image = models.ImageField(max_length=200, blank=False)
