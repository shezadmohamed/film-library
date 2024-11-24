from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.detail, name="detail"),
    path("<slug:slug>/reviews/", views.reviews, name="reviews")
]
