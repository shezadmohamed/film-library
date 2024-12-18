from django.urls import path, include
from . import views

app_name = 'layout'
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]
