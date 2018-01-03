__author__ = 'leif'
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


class AnitaConsent(models.Model):
    user = models.ForeignKey(User)
    agreed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class AnitaConsentForm(ModelForm):
    agreed = forms.BooleanField(label="Do you consent to participate in the study?", required=True)

    def clean(self):
        cleaned_data = super(AnitaConsentForm, self).clean()
        agreed = cleaned_data.get("agreed")
        if not agreed:
            raise forms.ValidationError("Consent not given.")
        return cleaned_data

    class Meta:
        model = AnitaConsent
        exclude = ('user',)


class AnitaDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(
        default=0,
        help_text="Please provide your age (in years).")

    # sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    status = models.CharField(max_length=100, default="")
    work = models.CharField(max_length=100, default="")
    level = models.CharField(max_length=3, default="")
    search_freq = models.IntegerField(
        default=0,
        help_text="How many times per week do you "
                  "conduct searches for information "
                  "(please enter a whole number)?")

    search_ability = models.CharField(default="", max_length=1)

    def __unicode__(self):
        return self.user.username


ED_CHOICES = \
    (
        ('', 'Not Specified'),
        ('GED', 'High School or GED'),
        ('ASS', "Associate's"),
        ('BCA', "Bachelor's"),
        ('MAS', "Master's"),
        ('PHD', "Doctorate")
    )

STATUS_CHOICES = \
    (
        ('', 'Not Specified'),
        ('staff', 'Staff'),
        ('undergrad', 'Undergraduate Student'),
        ('postgrad', 'Graduate Student')
    )


class AnitaDemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(
        label="Please provide your age (in years).",
        max_value=100,
        min_value=0,
        required=False)
    # sex = forms.CharField(
    # max_length=1,
    #     widget=forms.Select(
    #         choices=SEX_CHOICES),
    #            label="Please indicate your sex.",
    #            required=False)
    status = forms.CharField(
        widget=forms.Select(choices=STATUS_CHOICES),
        label="What is your status at University of Glasgow?",
        required=False)

    work = forms.CharField(
        widget=forms.TextInput(attrs={'size': '60', 'class': 'inputText'}),
        label="Please provide your occupation/major:", required=False)

    level = forms.CharField(
        max_length=3, widget=forms.Select(choices=ED_CHOICES),
        label="Please indicate the highest degree you've earned:", required=False)

    search_freq = forms.IntegerField(
        label="How many times per week do you conduct "
              "searches for information (please enter a whole number)?",
        max_value=10000, min_value=0, required=False)

    search_ability = forms.CharField(
        max_length=1, widget=forms.Select(choices=ABILITY_CHOICES),
        label="How would you rate your online search ability?", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0

        if not cleaned_data.get("search_freq"):
            cleaned_data["search_freq"] = 0

        return cleaned_data

    class Meta:
        model = AnitaDemographicsSurvey
        exclude = ('user',)


LIKERT_CHOICES = \
    (
        (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Strongly Agree')
    )


class AnitaPreTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_interested = models.IntegerField(default=0)
    apt_know = models.IntegerField(default=0)
    apt_clear_what = models.IntegerField(default=0)
    apt_info_diff = models.IntegerField(default=0)
    apt_sys_diff = models.IntegerField(default=0)
    apt_clear_how = models.IntegerField(default=0)
    apt_clear_steps = models.IntegerField(default=0)
    apt_difficult_finish = models.IntegerField(default=0)
    apt_task_diff = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPreTaskSurveyForm(ModelForm):
    apt_interested = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am interested in this topic.", required=False)
    apt_know = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES, label="I know a lot about this topic.",
        required=False)
    apt_clear_what = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="It is clear what information I need to complete the task.",
        required=False)
    apt_info_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I think it will be difficult to find relevant items for this task.",
        required=False)
    apt_sys_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I think it will be difficult to search for information using this system.",
        required=False)
    apt_clear_how = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="It is clear how much information I need to complete the task.",
        required=False)
    apt_clear_steps = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="It is clear which steps I need to take to complete this task.",
        required=False)
    apt_difficult_finish = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I think it will be difficult to determine when I have enough information to finish the task.",
        required=False)
    apt_task_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="Overall, I think this will be a difficult task.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPreTaskSurvey
        exclude = ('user', 'task_id', 'topic_num', 'condition')


class AnitaPostTask0Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    condition = models.IntegerField()
    apt_satisfied_amount = models.IntegerField(default=0)
    apt_satisfied_steps = models.IntegerField(default=0)
    apt_work_fast = models.IntegerField(default=0)
    apt_difficult_enough = models.IntegerField(default=0)
    apt_time_pressure = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask0SurveyForm(ModelForm):
    apt_satisfied_amount = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am satisfied with the amount of information I found for the search topic.",
        required=False)

    apt_satisfied_steps = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am satisfied with the steps I took to find information about the search topic.",
        required=False)

    apt_work_fast = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I needed to work fast to complete this task.", required=False)

    apt_difficult_enough = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought it was difficult to determine when I had enough information to finish the task.",
        required=False)

    apt_time_pressure = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt time pressure when completing this task.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask0Survey
        exclude = ('user', 'task_id', 'topic_num')


class AnitaPostTask1Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    condition = models.IntegerField()
    apt_search_diff = models.IntegerField(default=0)
    apt_hurried = models.IntegerField(default=0)
    apt_satisfied_systems = models.IntegerField(default=0)
    apt_doing_well = models.IntegerField(default=0)
    apt_found_enough = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask1SurveyForm(ModelForm):
    apt_search_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought it was difficult to search for information on this topic.",
        required=False)
    apt_hurried = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt hurried or rushed when completing this task.", required=False)
    apt_satisfied_systems = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am satisfied with how the system performed for this task.",
        required=False)
    apt_doing_well = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="While I was working on this task, I thought about how well I was doing on the task.",
        required=False)
    apt_found_enough = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found enough information about the search topic.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask1Survey
        exclude = ('user', 'task_id', 'topic_num','condition')


#
class AnitaPostTask2Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_accurate = models.IntegerField(default=0)
    apt_quick_results = models.IntegerField(default=0)
    apt_more_info = models.IntegerField(default=0)
    apt_time_left = models.IntegerField(default=0)
    apt_quick_task = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask2SurveyForm(ModelForm):
    apt_accurate = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="It was important to me to complete this task accurately.",
        required=False)

    apt_quick_results = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The system retrieved and displayed search results pages quickly.",
        required=False)

    apt_more_info = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I thought about how much information I had already "
              "found and how much more I still needed.",
        required=False)

    apt_time_left = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I thought about how much time I had left on the task. ",
        required=False)

    apt_quick_task = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="It was important to me to complete this task quickly.",
        required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask2Survey
        exclude = ('user', 'task_id', 'topic_num')


#
class AnitaPostTask3Survey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    apt_system_relevance = models.IntegerField(default=0)
    apt_system_download = models.IntegerField(default=0)
    apt_finding_diff = models.IntegerField(default=0)
    apt_all_info = models.IntegerField(default=0)
    apt_task_diff = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaPostTask3SurveyForm(ModelForm):
    apt_system_relevance = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="This system provided me with a great deal of relevant information.",
        required=False)
    apt_system_download = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="The system displayed the individual news articles quickly.",
        required=False)
    apt_finding_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought it was difficult to find relevant information on this topic.",
        required=False)
    apt_all_info = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found all of the information about the search topic in the search system.",
        required=False)
    apt_task_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="Overall, I thought this was a difficult task.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaPostTask3Survey
        exclude = ('user', 'task_id', 'topic_num')


class AnitaExit1Survey(models.Model):
    user = models.ForeignKey(User)
    ae_use_freq = models.IntegerField(default=0)
    ae_complex = models.IntegerField(default=0)
    ae_easy = models.IntegerField(default=0)
    ae_integrated = models.IntegerField(default=0)
    ae_inconsistent = models.IntegerField(default=0)
    ae_learn_quickly = models.IntegerField(default=0)
    ae_cumbersome = models.IntegerField(default=0)
    ae_confident = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class AnitaExit1SurveyForm(ModelForm):
    ae_use_freq = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I think that I would like to use this system frequently.", required=False)
    ae_complex = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found the system unnecessarily complex.", required=False)
    ae_easy = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought the system was easy to use.", required=False)
    ae_integrated = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found the various functions in the system to be well integrated.",
        required=False)
    ae_inconsistent = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought this system was too inconsistent.", required=False)
    ae_learn_quickly = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I would imagine that most people would learn to use this system very quickly.",
        required=False)
    ae_cumbersome = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found the system very cumbersome to use.", required=False)
    ae_confident = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt very confident using the system.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit1Survey
        exclude = ('user',)


EXTENT_CHOICES = \
    (
        (1, 'Not at all'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Very much')
    )


class AnitaExit2Survey(models.Model):
    user = models.ForeignKey(User)
    ae_time_extent = models.IntegerField(default=0)
    ae_time_reasonable = models.TextField(default="")
    ae_time_process = models.TextField(default="")
    ae_time_amount_found = models.TextField(default="")
    ae_time_amount_read = models.TextField(default="")
    ae_time_pressure_points = models.TextField(default="")

    def __unicode__(self):
        return self.user.username


class AnitaExit2SurveyForm(ModelForm):
    ae_time_extent = forms.ChoiceField(
        widget=RadioSelect, choices=EXTENT_CHOICES,
        label="To what extent did the amount of time you "
              "had to complete these task influence your performance?",
        required=False)
    ae_time_reasonable = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Do you think the time you had to complete these"
              " tasks was reasonable? Please explain.",
        required=False)
    ae_time_process = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the time you had to complete the tasks impact"
              " the process you used to complete the tasks "
              "(e.g., steps, thought process)? Please explain.",
        required=False)
    ae_time_amount_found = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the time you had to complete the tasks impact"
              " the amount of information you found? Please explain.",
        required=False)
    ae_time_amount_read = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the time you had to complete the tasks impact"
              " the extent to which you read the information that you found? Please explain.",
        required=False)
    ae_time_pressure_points = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="At what point(s) during the search tasks did you"
              " feel time pressure, if any? Please explain.",
        required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit2Survey
        exclude = ('user',)


class AnitaExit3Survey(models.Model):
    user = models.ForeignKey(User)
    ae_speed_compare = models.TextField(default="")
    ae_speed_process = models.TextField(default="")
    ae_speed_amount_found = models.TextField(default="")
    ae_speed_amount_read = models.TextField(default="")

    def __unicode__(self):
        return self.user.username


class AnitaExit3SurveyForm(ModelForm):
    ae_speed_compare = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="How did the speed of this system compare to others "
              "you have used? Please explain.",
        required=False)
    ae_speed_process = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the system speed impact the "
              "process you used to complete the tasks "
              "(e.g., steps, thought process)? Please explain.",
        required=False)
    ae_speed_amount_found = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the system speed impact the amount of "
              "information you found for the tasks? "
              "Please explain.",
        required=False)
    ae_speed_amount_read = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 6}),
        label="Did the system speed impact the extent "
              "to which you read the information "
              "that you found? Please explain.",
        required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = AnitaExit3Survey
        exclude = ('user',)


class MickeyPostTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    condition = models.IntegerField(default=0)
    interface = models.IntegerField(default=0)
    snip_readable = models.IntegerField(default=0)
    snip_confidence = models.IntegerField(default=0)
    snip_informativeness = models.IntegerField(default=0)
    snip_relevance = models.IntegerField(default=0)
    snip_clarity = models.IntegerField(default=0)
    snip_size = models.IntegerField(default=0)


    def __unicode__(self):
        return self.user.username


class MickeyPostTaskSurveyForm(ModelForm):
    snip_readable = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets (title, link and description) were not readable.",
        required=False)

    snip_confidence = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets increased my confidence in my decisions.",
        required=False)

    snip_informativeness = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets were not informative.",
        required=False)

    snip_relevance = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The results snippets help me judge the relevance of the document.",
        required=False)

    snip_clarity = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets were clear and concise.",
        required=False)


    snip_size = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets were not an appropriate size.",
        required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = MickeyPostTaskSurvey
        exclude = ('user', 'task_id', 'topic_num','condition')


class AnitaPreTaskResource(resources.ModelResource):

    class Meta:
        model = AnitaPreTaskSurvey
        exclude = ('id',)


class MickeyPostTaskResource(resources.ModelResource):

    class Meta:
        model = MickeyPostTaskSurvey
        exclude = ('id',)



class SnippetPostTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    condition = models.IntegerField()
    interface = models.IntegerField()
    #snip_helpfulness = models.IntegerField(default=0)
    snip_clarity = models.IntegerField(default=0)
    snip_confidence = models.IntegerField(default=0)
    snip_informativeness = models.IntegerField(default=0)
    snip_relevance = models.IntegerField(default=0)
    snip_readable = models.IntegerField(default=0)
    snip_size = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class SnippetPostTaskSurveyForm(ModelForm):
    snip_clarity = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets (title, link and description) were clear and concise.",
        required=False)


    snip_confidence = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets increased my confidence in my decisions.",
        required=False)

    snip_informativeness = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets were not informative.",
        required=False)

    snip_relevance = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The results snippets help me judge the relevance of the document.",
        required=False)

    snip_readable = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets  were not readable.",
        required=False)


    snip_size = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The result snippets were an appropriate size and length.",
        required=False)




    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SnippetPostTaskSurvey
        exclude = ('user', 'task_id', 'topic_num','condition','interface')


class SnippetPostTaskResource(resources.ModelResource):

    class Meta:
        model = SnippetPostTaskSurvey
        exclude = ('id',)





class SystemSnippetPostTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    condition = models.IntegerField()
    interface = models.IntegerField()
    apt_accurate = models.IntegerField()
    apt_quick_results = models.IntegerField()
    apt_search_diff = models.IntegerField()
    apt_hurried = models.IntegerField()
    apt_satisfied_systems = models.IntegerField()
    ae_cumbersome = models.IntegerField()
    ae_confident = models.IntegerField()

    def __unicode__(self):
        return self.user.username


class SystemSnippetPostTaskSurveyForm(ModelForm):

    apt_accurate = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="It was important to me to complete this task accurately.",
        required=True)

    apt_quick_results = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The system retrieved and displayed search results pages quickly.",
        required=True)

    apt_search_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought it was difficult to search for information on this topic.",
        required=True)

    apt_hurried = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt rushed when completing this task.", required=True)

    apt_satisfied_systems = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am satisfied with how the system performed for this task.",
        required=True)

    ae_cumbersome = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found the system very cumbersome to use.", required=True)

    ae_confident = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt very confident using the system.", required=True)



    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SystemSnippetPostTaskSurvey
        exclude = ('user', 'task_id', 'topic_num','condition','interface')


class SystemSnippetPostTaskResource(resources.ModelResource):

    class Meta:
        model = SystemSnippetPostTaskSurvey
        exclude = ('id',)


SEARCH_FREQ = (('','Not Specified'), (6, 'Many times a day'),
                (5,'1-2 times a day'), (4,'A many times a week'), (3,'A few times a week'),
                (2,'Sometimes'), (1,'Rarely'), (0,'Never'), )


DEVICES = (('','Not Specified'),('MS','Mouse with Scroll Wheel/Gesture'),('M','Mouse'),('TS','Trackpad with Scroll/Gesture'), ('T','Trackpad'), ('O','Other') )

ENGINES = ( ('','Not Specified'),('AOL','AOL'),('BAI','Baidu'),('BIN','Bing'), ('GOO','Google'), ('YAH','Yahoo!'), ('OTH','Other') )



class SnippetDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(
        help_text="Please provide your age (in years).")

    sex = models.CharField(max_length=1, choices = SEX_CHOICES, help_text="Please indicate your sex.")
    work = models.CharField(max_length=100)
    level = models.CharField(max_length=3)

    search_freq = models.IntegerField()

    news_search_freq = models.IntegerField()

    input_device = models.CharField(max_length=2)

    search_engine = models.CharField(max_length=3)

    def __unicode__(self):
        return self.user.username

class SnippetDemographicsSurveyForm(ModelForm):
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


SNIP_CHOICES = ((0, 'Title Only'),(1, 'Title + 1 line summary)'),
                (2,'Title + 1-2 lines summary)'), (3,'Title + 2-3 line summary'))




class SnippetExitSurvey(models.Model):
    user = models.ForeignKey(User)
    snip_info = models.IntegerField()
    snip_easy = models.IntegerField()
    snip_help = models.IntegerField()
    snip_useful = models.IntegerField()
    snip_prefer = models.IntegerField()
    snip_why = models.TextField()
    snip_improve = models.TextField()


    def __unicode__(self):
        return self.user.username


class SnippetExitSurveyForm(ModelForm):
    snip_info = forms.ChoiceField(
        widget=RadioSelect, choices=SNIP_CHOICES,
        label="The most informative result summaries were:", required=True)
    snip_easy = forms.ChoiceField(
        widget=RadioSelect, choices=SNIP_CHOICES,
        label="The unhelpful result summaries were:", required=True)
    snip_help = forms.ChoiceField(
        widget=RadioSelect, choices=SNIP_CHOICES,
        label="The easiest result summaries to use were:", required=True)
    snip_useful = forms.ChoiceField(
        widget=RadioSelect, choices=SNIP_CHOICES,
        label="The least useful result summaries were:",
        required=True)
    snip_prefer = forms.ChoiceField(
        widget=RadioSelect, choices=SNIP_CHOICES,
        label="The most preferable type of result summaries for such tasks were:",
        required=True)

    snip_why = forms.CharField(widget=Textarea,
                               label="Given your last answer, explain why you prefer result summaries of this length.",
                               required=True)
    snip_improve = forms.CharField(widget=Textarea,
                                label="Please provide suggestions on how this study could be improved.",
                                required=True)



    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SnippetExitSurvey
        exclude = ('user',)



class SnippetPreTaskTopicKnowledgeSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    condition = models.IntegerField()
    interface = models.IntegerField()
    topic_knowledge = models.IntegerField()
    topic_relevance = models.IntegerField()
    topic_interest = models.IntegerField()
    topic_searched = models.IntegerField()
    topic_difficulty = models.IntegerField()

    def __unicode__(self):
        return self.user.username


TOPIC_NOTHING_CHOICES = ( (1, 'Nothing'), (2, ''), (3, ''), (4, ''), (5, 'I Know Details')  )
TOPIC_NOTATALL_CHOICES = ( (1, 'Not at all'), (2, ''), (3, ''), (4, ''), (5, 'Very Much')  )
TOPIC_NEVER_CHOICES = ( (1, 'Never'), (2, ''), (3, ''), (4, ''), (5, 'Very Often')  )
TOPIC_EASY_CHOICES = ( (1, 'Very Easy'), (2, ''), (3, ''), (4, ''), (5, 'Very Difficult')  )
TOPIC_NOTGOOD_CHOICES = ( (1, 'Not Good'), (2, ''), (3, ''), (4, ''), (5, 'Very Good')  )
TOPIC_UNSUCCESSFUL_CHOICES = ( (1, 'Unsuccessful'), (2, ''), (3, ''), (4, ''), (5, 'Successful')  )
TOPIC_FEW_CHOICES = ( (1, 'A few of them'), (2, ''), (3, ''), (4, ''), (5, 'All of them')  )


class SnippetPreTaskTopicKnowledgeSurveyForm(ModelForm):

    topic_knowledge = forms.ChoiceField(widget=RadioSelect,
                                        choices=TOPIC_NOTHING_CHOICES,
                                        label="How much do you know about this topic?",
                                        required=True)
    topic_relevance = forms.ChoiceField(widget=RadioSelect,
                                        choices=TOPIC_NOTATALL_CHOICES,
                                        label="How relevant is this topic to your life?",
                                        required=True)
    topic_interest = forms.ChoiceField(widget=RadioSelect,
                                       choices=TOPIC_NOTATALL_CHOICES,
                                       label="How interested are you to learn more about this topic?",
                                       required=True)
    topic_searched = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NEVER_CHOICES,
                                       label="Have you ever searched for information related to this topic?",
                                       required=True)
    topic_difficulty = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                         label="How difficult do you think it will be to search for information about this topic?",
                                         required=True)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SnippetPreTaskTopicKnowledgeSurvey
        exclude = ('user', 'task_id', 'topic_num','condition','interface')

########################################
# DIVERSITY POST TASK SURVEYS
#
########################################

class BehaveDiversityPostTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    condition = models.IntegerField()
    interface = models.IntegerField()
    diversity = models.IntegerField()
    beh_div_success = models.IntegerField(default=0)
    beh_div_speed = models.IntegerField(default=0)
    beh_div_queries = models.IntegerField(default=0)
    beh_div_documents = models.IntegerField(default=0)
    beh_div_time = models.IntegerField(default=0)
    beh_div_marked = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class BehaveDiversityPostTaskSurveyForm(ModelForm):
    beh_div_success = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I was able to complete the search task successfully.",
        required=False)


    beh_div_speed = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I was able the complete the search task quickly.",
        required=False)

    beh_div_queries = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I issued more queries than I expected.",
        required=False)

    beh_div_documents= forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I examined more document than I expected.",
        required=False)

    beh_div_time = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I spent more time reading documents than I expected.",
        required=False)


    beh_div_marked = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="I marked more documents as relevant than I needed.",
        required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = BehaveDiversityPostTaskSurvey
        exclude = ('user', 'task_id', 'topic_num','condition','interface','diversity')



class SystemDiversityPostTaskSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    condition = models.IntegerField()
    interface = models.IntegerField()
    diversity = models.IntegerField()
    apt_accurate = models.IntegerField()
    apt_quick_results = models.IntegerField()
    apt_search_diff = models.IntegerField()
    apt_time = models.IntegerField()
    apt_satisfied_systems = models.IntegerField()
    ae_cumbersome = models.IntegerField()
    ae_confident = models.IntegerField()

    def __unicode__(self):
        return self.user.username


class SystemDiversityPostTaskSurveyForm(ModelForm):

    apt_accurate = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="It was important to me to complete this task accurately.",
        required=True)

    apt_quick_results = forms.ChoiceField(
        widget=RadioSelect,
        choices=LIKERT_CHOICES,
        label="The system retrieved and displayed search results pages quickly.",
        required=True)

    apt_search_diff = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I thought it was difficult to search for information on this topic.",
        required=True)

    apt_time = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="The system helped me to complete my task sooner.", required=True)

    apt_satisfied_systems = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I am satisfied with how the system performed for this task.",
        required=True)

    ae_cumbersome = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I found the system very cumbersome to use.", required=True)

    ae_confident = forms.ChoiceField(
        widget=RadioSelect, choices=LIKERT_CHOICES,
        label="I felt very confident using the system.", required=True)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SystemDiversityPostTaskSurvey
        exclude = ('user', 'task_id', 'topic_num','condition','interface','diversity')


########################################
# DIVERSITY POST EXPERIMENT SURVEYS
#
########################################


DIVERSITY_CHOICES = ((1, 'Definitely A '),(2, 'Mostly A'), (3, 'Slightly A'),
                (4,'Slightly B'), (5,'Mostly B'), (6,'Definitely B') )


class DiversityExitSurvey(models.Model):
    user = models.ForeignKey(User)
    div_info = models.IntegerField()
    div_easy = models.IntegerField()
    div_help = models.IntegerField()
    div_useful = models.IntegerField()
    div_prefer = models.IntegerField()
    div_relevance_prefer = models.IntegerField()
    div_diversity_prefer = models.IntegerField()
    div_why = models.TextField()
    div_improve = models.TextField()


    def __unicode__(self):
        return self.user.username


class DiversityExitSurveyForm(ModelForm):
    div_info = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The most informative system was:", required=True)
    div_easy = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The most unhelpful system was:", required=True)
    div_help = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The easiest system to use was:", required=True)
    div_useful = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The least useful system was:",
        required=True)

    div_relevance_prefer = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The system that returned the most relevant information was:",
        required=True)

    div_diversity_prefer = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The system that returned the most diverse information was:",
        required=True)

    div_prefer = forms.ChoiceField(
        widget=RadioSelect, choices=DIVERSITY_CHOICES,
        label="The most preferable system overall was:",
        required=True)


    div_why = forms.CharField(widget=Textarea,
                               label="Given your last answer, explain why you prefer result summaries of this length.",
                               required=True)
    div_improve = forms.CharField(widget=Textarea,
                                label="Please provide suggestions on how this study could be improved.",
                                required=True)



    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = DiversityExitSurvey
        exclude = ('user',)
