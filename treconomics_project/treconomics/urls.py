from snippets import views

__author__ = 'leif'

from django.conf.urls import patterns, url
import views
from .views import PreExperimentView
from .views import PostExperimentView
from .views import TaskSpacerView
from .views import EndExperimentView
from .views import SessionCompletedView
from search import views as search_views
from snippets import views as snippet


urlpatterns = \
    patterns('',
             url(r'^$', views.view_amt_login, name='home'),
             url(r'^login/$', views.view_amt_login, name='login'),
             url(r'^register/$', views.view_register_amt_user, name='register-amt-user'),
             url(r'^logout/$', views.view_logout, name='logout'),
             url(r'^next/$', views.view_next, name='next'),
             url(r'^startexperiment/$', views.start_amt_experiment, name='start-experiment'),
             url(r'^preexperiment/(?P<version>[A-Z]{2})/$', PreExperimentView.as_view(), name='pre-experiment'),
             url(r'^pretask/(?P<taskid>\d+)/$', views.pre_task, name='pre-task'),
             url(r'^prepracticetask/(?P<taskid>\d+)/$', views.pre_practice_task),
             url(r'^pretaskquestions/(?P<taskid>\d+)/$', views.pre_task_with_questions),
             url(r'^(?P<whoosh_docid>\d+)/$', search_views.show_document),
             url(r'^saved/$', search_views.show_saved_documents, name='saved'),
             url(r'^search/$', search_views.search, name='search'),
             url(r'^search/(?P<taskid>\d+)/$', search_views.search, name='search-task'),
             url(r'^posttask/(?P<taskid>\d+)/$', views.post_task, name='post-task'),
             url(r'^postpracticetask/(?P<taskid>\d+)/$', views.post_practice_task),
             url(r'^posttaskquestions/(?P<taskid>\d+)/$', views.post_task_with_questions),

             url(r'^showtask/$', views.show_task),
             url(r'^sessioncommence/$', views.commence_session),
             url(r'^taskspacer/$', TaskSpacerView.as_view()),
             url(r'^taskspacerwithdetails/(?P<taskid>\d+)/$', views.task_spacer_with_details),
             url(r'^taskspacer2/(?P<msg_id>\d+)/$', views.task_spacer_msg),

             url(r'^sessioncompleted/$', SessionCompletedView.as_view(), name='session-completed'),
             url(r'^postexperiment/$', PostExperimentView.as_view()),
             url(r'^endexperiment/$', EndExperimentView.as_view()),

             url(r'^performance/$', search_views.view_performance),
             url(r'^suggestion_selected/$', search_views.suggestion_selected),
             url(r'^suggestion_hover/$', search_views.suggestion_hover),
             url(r'^query_focus/$', search_views.view_log_query_focus),
             url(r'^hover/$', search_views.view_log_hover),
             url(r'^autocomplete/$', search_views.autocomplete_suggestion),

             url(r'^reset/$', views.reset_test_users),
             url(r'^querytest/(?P<topic_num>\d+)/$', search_views.view_run_queries),
             url(r'^timeout/$', views.show_timeout_message, name='timeout'),

             # (r'^demographicssurvey/(?P<country>[A-Z]{2})/$', survey_views.view_demographics_survey),
             # (r'^searchefficacysurvey/$', survey_views.view_search_efficacy_survey),
             # (r'^nasaloadsurvey/$', survey_views.view_nasa_load_survey),
             # (r'^nasaqueryloadsurvey/$', survey_views.view_nasa_query_load_survey),
             # (r'^nasanavigationloadsurvey/$', survey_views.view_nasa_navigation_load_survey),
             # (r'^nasaassessmentloadsurvey/$', survey_views.view_nasa_assessment_load_survey),
             # (r'^nasafactorcomparesurvey/$', survey_views.view_nasa_factor_compare_survey),
             # (r'^conceptlistingsurvey/(?P<taskid>\d+)/(?P<when>[A-Z]{3})/$',
             # survey_views.view_concept_listing_survey),
             # (r'^shortstresssurvey/$', survey_views.view_short_stress_survey),
             # (r'^modifiedstresssurvey/$', survey_views.view_modified_stress_survey),

             url(r'^snippetposttask/(?P<taskid>\d+)/$', snippet.view_snippet_posttask),
             url(r'^systemsnippetposttask/(?P<taskid>\d+)/$', snippet.view_system_snippet_posttask),
             url(r'^snippetpretask/(?P<taskid>\d+)/$', snippet.view_snippet_pretask),
             url(r'^demographicssurvey/$', snippet.view_alt_demographic_survey, name='demographics'),
             url(r'^snippetexitsurvey/$', snippet.view_snippet_exit_survey, name='snippet-exit-survey'),

            # new surveys added for diversity study
             url(r'^diversityendstats/(?P<taskid>\d+)/$', snippet.diversity_end_stats),
             url(r'^diversityposttask/(?P<taskid>\d+)/$', snippet.view_diversity_posttask),
             url(r'^systemdiversityposttask/(?P<taskid>\d+)/$', snippet.view_system_diversity_posttask),
             url(r'^diversityexitsurvey/$', snippet.view_diversity_exit_survey, name='diversity-exit-survey'),
             url(r'^diversityperformance/$', search_views.view_performance_diversity),  # New diversity performance view
             url(r'^diversityperformancepractice/$', search_views.view_performance_diversity_practice),  # New practice performance view

             url(r'^showusers/$', views.show_users, name='showusers'),
             url(r'^showuserperformance/(?P<userid>\d+)/$', views.show_user_performance, name='showuserperformance'),


             (r'^anitapretasksurvey/(?P<taskid>\d+)/$', snippet.view_alt_pretask_survey),
             (r'^anitaposttask0survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask0_survey),
             (r'^anitaposttask1survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask1_survey),
             (r'^anitaposttask2survey/(?P<taskid>\d+)/$', snippet.view_anita_posttask2_survey),
             (r'^anitaposttask3survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask3_survey),

             (r'^anitaexit1survey/$', snippet.view_alt_exit1_survey),
             (r'^anitaexit2survey/$', snippet.view_alt_exit2_survey),
             (r'^anitaexit3survey/$', snippet.view_alt_exit3_survey),
             (r'^consent/$', snippet.view_consent),

    )
