from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Film

def index(request):
    film_list = Film.objects.order_by("-release_year")
    template = loader.get_template("films/index.html")
    context = {
        "film_list": film_list,
    }
    return HttpResponse(template.render(context, request))

def film_detail(request, film_id):
    film_name = Film.objects.get(pk=film_id)
    return HttpResponse("This is the homepage for %s." % film_name)

def film_reviews(request, film_id):
    film_name = Film.objects.get(pk=film_id)
    return HttpResponse("These are the reviews for %s." % film_name)
