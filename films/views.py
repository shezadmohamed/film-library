from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from django.template import loader
from .models import Film, Review

def index(request):
    film_list = Film.objects.order_by("-release_year")
    context = {
        "film_list": film_list,
    }
    return render(request, "films/index.html", context)

def detail(request, slug):
    film = get_object_or_404(Film, slug=slug)
    print("got here")
    if request.method == 'POST':
        if request.POST["review_date"]:
            new_review = Review(film=film,
                                review_text=request.POST["review_text"],
                                review_date=request.POST["review_date"])
            new_review.save()
            return HttpResponseRedirect(reverse("films:reviews", args=[slug]))
        else:
            return render(
                request,
                "films/detail.html",
                {"film": film, "error_message": "Select a date."}
            )
    else:
        return render(request, "films/detail.html",
                        {"film": film, "error_message": ""}
        )

def reviews(request, slug):
    film = get_object_or_404(Film, slug=slug)
    return render(request, "films/reviews.html", {"film": film, "review_set": film.review_set.all().order_by("-review_date")})
