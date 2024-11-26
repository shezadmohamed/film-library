from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

# from django.template import loader
from .models import Film, Review
from .forms import AddReviewForm


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


def index(request):
    film_list = Film.objects.order_by("-release_year")
    context = {
        "film_list": film_list,
    }
    return render(request, "films/index.html", context)


@login_required
def detail(request, slug):
    film = get_object_or_404(Film, slug=slug)

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            new_review = Review(film=film,
                                review_text=form.cleaned_data["review_text"],
                                review_date=form.cleaned_data["review_date"])
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
