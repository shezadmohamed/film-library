from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title_id>/", views.detail, name="detail"),
    path("<str:title_id>/reviews/", views.reviews, name="reviews")
]
