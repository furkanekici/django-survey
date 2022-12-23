from django.db import models
from accounts.models import CustomUser


class Question(models.Model):

    questionText = models.CharField(max_length=100)
    participationCount = models.IntegerField(default=0)
    yesCount = models.IntegerField(default=0)
    noCount = models.IntegerField(default=0)
    otherCount = models.IntegerField(default=0)

    def __str__(self):
        return self.questionText


class Answer(models.Model):
    toQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    responseText = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.responseText
