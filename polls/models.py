from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('date published')
    for_kids = models.BooleanField(default=False)
    high_activity = models.BooleanField(default=False)
