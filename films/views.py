from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
import re

# from django.template import loader
from .models import Film, Review
from .forms import AddReviewForm
from .constants import BEARER_KEY


class FilmIndexView(generic.ListView):
    model = Film
    template_name = "films/index.html"
    ordering = "-release_year"


class ReviewListByFilmView(generic.ListView):
    template_name = "films/reviews.html"
    context_object_name = "review_set"

    def get_queryset(self):
        self.film = get_object_or_404(Film, slug=self.kwargs["slug"])
        print(self.film)
        return Review.objects.filter(film=self.film).order_by("-review_date")

    def get_context_data(self, **kwargs):
        self.film = get_object_or_404(Film, slug=self.kwargs["slug"])
        context = super().get_context_data(**kwargs)
        context["film"] = self.film
        return context


class ReviewCreateClass(generic.edit.CreateView):
    form_class = AddReviewForm
    template_name = "films/add_review.html"
    # success_url = reverse("films:reviews", args=[self.kwargs["slug"]])

    def get_context_data(self, **kwargs):
        self.film = get_object_or_404(Film, slug=self.kwargs["slug"])
        context = super().get_context_data(**kwargs)
        context["film"] = self.film
        return context
    

class ReviewListByUser(LoginRequiredMixin, generic.ListView):
    template_name = "films/user_reviews.html"
    context_object_name = "review_set"

    def get_queryset(self) -> QuerySet[Any]:
        return Review.objects.filter(reviewer=self.request.user).order_by("-review_date")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


def index(request):
    print("got here")
    film_list = Film.objects.order_by("-release_year")
    context = {
        "film_list": film_list,
    }
    if request.method == 'POST':
        print(list(request.POST.keys()))
        if 'submit-search' in request.POST:
            search_query = request.POST['search-query']
            search_query = re.sub(" ", "%20", search_query)
            search_results = film_search(search_query)
            context['search_results'] = [
                (result['title'], f"https://image.tmdb.org/t/p/w185{result['poster_path']}", result['id']) 
                for result in search_results
                ]
        
            return render(request, "films/index.html", context)
        for i in range(3):
            if f'add-film{i}' in request.POST:
                pass
    return render(request, "films/index.html", context)


@login_required
def detail(request, slug):
    film = get_object_or_404(Film, slug=slug)

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            new_review = Review(film=film,
                                review_text=form.cleaned_data["review_text"],
                                review_date=form.cleaned_data["review_date"],
                                reviewer=request.user)
            new_review.save()
            return HttpResponseRedirect(reverse("films:reviews", args=[slug]))
        else:
            return render(request,
                          "films/add_review.html",
                          {"film": film,
                           "error_message": "Select a date.",
                           "form": form
                           }
                          )
    else:
        form = AddReviewForm()
        return render(request,
                      "films/add_review.html",
                      {"film": film,
                       "error_message": "",
                       "form": form
                       }
                      )


def reviews(request, slug):
    film = get_object_or_404(Film, slug=slug)
    return render(request,
                  "films/reviews.html",
                  {"film": film, "review_set": film.review_set.all().order_by("-review_date")}
                  )


def film_search(query):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}"
    headers = {"accept": "application/json",
               "Authorization": BEARER_KEY
    }
    search_results = requests.get(url, headers=headers).json()['results'][0:3]
    return [{'title': result['title'],
             'poster_path': result['poster_path'],
             'year': result['release_date'][0:4],
             'id': result['id']} for result in search_results]