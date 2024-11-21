from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="films_index"),
    path("<int:film_id>/", views.film_detail, name="film_detail"),
    path("<int:film_id>/reviews/", views.film_reviews, name="film_reviews")
]
