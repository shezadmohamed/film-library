from django import forms
from .models import Film, Review


class AddReviewForm(forms.Form):
    review_text = forms.CharField(label="Review:", max_length=5000, widget=forms.Textarea)
    review_date = forms.DateField(label="Date:", widget=forms.DateInput(attrs={'type': 'date'}))
