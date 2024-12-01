from django import forms
from .models import Film, Review


class AddReviewForm(forms.Form):
    review_text = forms.CharField(label="Review:",
                                  max_length=5000,
                                  widget=forms.Textarea(attrs={'rows': '2', 'cols': '50'}))
    review_date = forms.DateField(label="Date:",
                                  widget=forms.DateInput(attrs={'type': 'date', 'cols': '10'}))
