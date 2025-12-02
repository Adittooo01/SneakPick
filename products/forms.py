
from django import forms

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write a review (optional)', 'rows': 4}), required=False)