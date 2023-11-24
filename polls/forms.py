from django import forms
from .models import Location, Language


class ArticleFilterForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="All Locations", required=False)
    language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="All Languages", required=False)
    for_kids = forms.BooleanField(required=False, initial=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    high_activity = forms.BooleanField(required=False, initial=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    free = forms.BooleanField(required=False, initial=False,
                              widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super(ArticleFilterForm, self).__init__(*args, **kwargs)
        self.fields['location'].label_from_instance = lambda obj: obj.name
        self.fields['language'].label_from_instance = lambda obj: obj.name