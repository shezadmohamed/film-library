from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path("", views.FilmIndexView.as_view(), name="index"),
    path("<slug:slug>/", views.detail, name="detail"),
    path("<slug:slug>/reviews/", views.ReviewListByFilmView.as_view(), name="reviews")
]
