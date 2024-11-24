from django.db import models
from django.utils import timezone
import datetime
import re

class Film(models.Model):
    film_title = models.CharField(max_length=200)
    release_year = models.SmallIntegerField()
    title_id = models.CharField(max_length=200, default="")

    def __str__(self):
        return f'{self.film_title} ({self.release_year})'

    def save(self, *args, **kwargs):
        self.title_id = self._get_text_id()
        super(Film, self).save(*args, **kwargs)

    def _get_text_id(self):
        return re.sub("[^a-zA-Z0-9]", "", self.film_title).lower() + str(self.release_year)

class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=5000)
    review_date = models.DateField()

    def __str__(self):
        return f'Review of {self.film} on {self.review_date}: {self.review_text}'

    def was_published_recently(self):
        return self.review_date >= timezone.localtime().date() - datetime.timedelta(days=30)


def _film_title_to_text_id(title, year):
    return re.sub("[^a-zA-Z0-9]", "", title).lower() + str(year)
