import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class PollUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)


    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class ApiKey(models.Model):
    username = models.CharField(max_length=50)
    api_key = models.CharField(max_length=20)

    def __str__(self):
        return "{} - {}".format(self.username, self.api_key)

