from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)


class Language(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    for_kids = models.BooleanField(default=False)
    high_activity = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    free = models.BooleanField(default=False)
    slot1_remaining_count = models.IntegerField(default=20)
    slot2_remaining_count = models.IntegerField(default=20)
    slot3_remaining_count = models.IntegerField(default=20)
