"""Models for English trainer app"""

from django.db import models


class Word(models.Model):
    """Word model for training system"""

    english = models.CharField(max_length=100)
    russian = models.CharField(max_length=100)
    example = models.TextField(blank=True)

    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

    def __str__(self):
        return str(self.english)