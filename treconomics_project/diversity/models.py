__author__ = 'yashar'
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from django.forms.widgets import RadioSelect, Textarea
from import_export import resources

from survey.forms import clean_to_zero


SEX_CHOICES = \
    (
        ('N', 'Not Indicated'),
        ('M', 'Male'), ('F', 'Female'), ('O', 'Other')
    )

YES_CHOICES = \
    (
        ('', 'Not Specified'),
        ('Y', 'Yes'), ('N', 'No')
    )

YES_NO_CHOICES = \
    (
        ('Y', 'Yes'), ('N', 'No')
    )

STANDING_CHOICES = \
    (
        ('', 'Not Specified'),
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior')
    )

YEAR_CHOICES = \
    (
        ('', 'Not Specified'),
        ('1', 'First Year'), ('2', 'Second Year'),
        ('3', 'Third Year'), ('4', 'Fourth Year'),
        ('5', 'Fifth Year'), ('6', 'Completed')
    )

ABILITY_CHOICES = \
    (
        ('0', 'Not Specified'),
        ('1', '1 - Novice'),
        ('2', '2'), ('3', '3'),
        ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7 - Expert')
    )

# Feel free to add the classes for the surveys here.
# There are some potential answers you can choose from above -- or you can create your own set if you wish.
# Feel free to copy from the existing snippet models.py classes as required -- the demographics class below has been directly copied without modification (except for renaming the class).

class DiversityDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(
        label="Please provide your age (in years).",
        max_value=100,
        min_value=18,
        required=True)

    sex = forms.CharField(
     max_length=1,
         widget=forms.Select(
             choices=SEX_CHOICES),
                label="Please indicate your gender.",
                required=True)

    work = forms.CharField(
        widget=forms.TextInput(attrs={'size': '60', 'class': 'inputText'}),
        label="Please provide your occupation:", required=True)

    level = forms.CharField(
        max_length=3, widget=forms.Select(choices=ED_CHOICES),
        label="Please indicate the highest degree you've been awarded:", required=True)

    search_freq = forms.IntegerField( widget=forms.Select(choices=SEARCH_FREQ),
        label="How often do you search the web?",
        max_value=7, min_value=-1, required=True)

    news_search_freq = forms.IntegerField( widget=forms.Select(choices=SEARCH_FREQ),
        label="How often do you search the web for news articles?",
        max_value=7, min_value=-1, required=True)


    search_engine = forms.CharField( widget=forms.Select(choices=ENGINES),
        label="What search engine do you typically use?",
        max_length=3, required=True)

    input_device = forms.CharField( widget=forms.Select(choices=DEVICES),
        label="What kinds of pointing device are you using?",
        max_length=2, required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0

        return cleaned_data

    class Meta:
        model = SnippetDemographicsSurvey
        exclude = ('user',)