from django.db import models

# Create your models here.
class Answer(models.Model):
    answer_text = models.CharField(max_length=500)
    has_api = models.BooleanField(default=False)
    api = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.answer_text

class Question(models.Model):
    question_text = models.CharField(max_length=300)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
