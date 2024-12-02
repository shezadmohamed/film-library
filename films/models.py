from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

import datetime
import re

class Film(models.Model):
    film_title = models.CharField(max_length=200)
    release_year = models.SmallIntegerField()
    tmdb_id = models.IntegerField(null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.film_title} ({self.release_year})'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self._slugify()
        super(Film, self).save(*args, **kwargs)

    def _slugify(self):
        return re.sub("[^a-zA-Z0-9]", "", self.film_title).lower() + str(self.release_year)

class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=5000)
    review_date = models.DateField()
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                 on_delete=models.SET_NULL, 
                                 null=True, 
                                 blank=True)

    def __str__(self):
        return f'Review of {self.film} on {self.review_date}: {self.review_text}'

    def get_absolute_url(self):
        return reverse("reviews", kwargs={"slug": self.film.slug})

    def was_published_recently(self):
        return self.review_date >= timezone.localtime().date() - datetime.timedelta(days=30)


def _film_title_to_text_id(title, year):
    return re.sub("[^a-zA-Z0-9]", "", title).lower() + str(year)
