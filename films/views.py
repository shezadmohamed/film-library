from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# from django.template import loader
from .models import Film, Review

def index(request):
    film_list = Film.objects.order_by("-release_year")
    context = {
        "film_list": film_list,
    }
    return render(request, "films/index.html", context)

def detail(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    return render(request, "films/detail.html", {"film": film})

def reviews(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    return render(request, "films/reviews.html", {"film": film})
    return HttpResponse("These are the reviews for %s." % film_name)
