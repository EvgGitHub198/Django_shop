from django import forms
from catalog.models import Review


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, label='Поиск')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'advantages', 'disadvantages', 'comment', 'rating']