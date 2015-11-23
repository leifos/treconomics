# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptListingSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('when', models.CharField(default=b'', max_length=4)),
                ('concepts', models.TextField(default=0)),
                ('paragraph', models.TextField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModifiedStressSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stress_confident', models.IntegerField(default=0)),
                ('stress_alert', models.IntegerField(default=0)),
                ('stress_irritated', models.IntegerField(default=0)),
                ('stress_others', models.IntegerField(default=0)),
                ('stress_angry', models.IntegerField(default=0)),
                ('stress_proficient', models.IntegerField(default=0)),
                ('stress_grouchy', models.IntegerField(default=0)),
                ('stress_concerned', models.IntegerField(default=0)),
                ('stress_committed', models.IntegerField(default=0)),
                ('stress_annoyed', models.IntegerField(default=0)),
                ('stress_impatient', models.IntegerField(default=0)),
                ('stress_self_conscious', models.IntegerField(default=0)),
                ('stress_control', models.IntegerField(default=0)),
                ('stress_sad', models.IntegerField(default=0)),
                ('stress_active', models.IntegerField(default=0)),
                ('stress_motivated', models.IntegerField(default=0)),
                ('stress_dissatisfied', models.IntegerField(default=0)),
                ('stress_performance', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NasaFactorCompare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NasaSystemLoad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nasa_mental_demand', models.IntegerField(default=0)),
                ('nasa_physical_demand', models.IntegerField(default=0)),
                ('nasa_temporal', models.IntegerField(default=0)),
                ('nasa_performance', models.IntegerField(default=0)),
                ('nasa_effort', models.IntegerField(default=0)),
                ('nasa_frustration', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NasaQueryLoad',
            fields=[
                ('nasasystemload_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.NasaSystemLoad')),
            ],
            options={
            },
            bases=('survey.nasasystemload',),
        ),
        migrations.CreateModel(
            name='NasaNavigationLoad',
            fields=[
                ('nasasystemload_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.NasaSystemLoad')),
            ],
            options={
            },
            bases=('survey.nasasystemload',),
        ),
        migrations.CreateModel(
            name='NasaAssessmentLoad',
            fields=[
                ('nasasystemload_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.NasaSystemLoad')),
            ],
            options={
            },
            bases=('survey.nasasystemload',),
        ),
        migrations.CreateModel(
            name='PostConceptListingSurvey',
            fields=[
                ('conceptlistingsurvey_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='survey.ConceptListingSurvey')),
            ],
            options={
            },
            bases=('survey.conceptlistingsurvey',),
        ),
        migrations.CreateModel(
            name='PostTaskTopicRatingSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('relevance_difficulty', models.IntegerField(default=0)),
                ('relevance_skill', models.IntegerField(default=0)),
                ('relevance_system', models.IntegerField(default=0)),
                ('relevance_success', models.IntegerField(default=0)),
                ('relevance_number', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreTaskTopicKnowledgeSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('topic_knowledge', models.IntegerField(default=0, help_text=b'How much do you know about this topic?')),
                ('topic_relevance', models.IntegerField(default=0)),
                ('topic_interest', models.IntegerField(default=0)),
                ('topic_searched', models.IntegerField(default=0)),
                ('topic_difficulty', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchEfficacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('efficacy_identify_requirements', models.IntegerField(default=0)),
                ('efficacy_develop_queries', models.IntegerField(default=0)),
                ('efficacy_special_syntax', models.IntegerField(default=0)),
                ('efficacy_evaluate_list', models.IntegerField(default=0)),
                ('efficacy_many_relevant', models.IntegerField(default=0)),
                ('efficacy_enough_results', models.IntegerField(default=0)),
                ('efficacy_like_a_pro', models.IntegerField(default=0)),
                ('efficacy_few_irrelevant', models.IntegerField(default=0)),
                ('efficacy_structure_time', models.IntegerField(default=0)),
                ('efficacy_focus_query', models.IntegerField(default=0)),
                ('efficacy_distinguish_relevant', models.IntegerField(default=0)),
                ('efficacy_competent_effective', models.IntegerField(default=0)),
                ('efficacy_little_difficulty', models.IntegerField(default=0)),
                ('efficacy_allocated_time', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShortStressSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stress_confident', models.IntegerField(default=0)),
                ('stress_alert', models.IntegerField(default=0)),
                ('stress_others', models.IntegerField(default=0)),
                ('stress_figure', models.IntegerField(default=0)),
                ('stress_angry', models.IntegerField(default=0)),
                ('stress_proficient', models.IntegerField(default=0)),
                ('stress_irritated', models.IntegerField(default=0)),
                ('stress_grouchy', models.IntegerField(default=0)),
                ('stress_reflecting', models.IntegerField(default=0)),
                ('stress_concerned', models.IntegerField(default=0)),
                ('stress_committed', models.IntegerField(default=0)),
                ('stress_annoyed', models.IntegerField(default=0)),
                ('stress_impatient', models.IntegerField(default=0)),
                ('stress_self_conscious', models.IntegerField(default=0)),
                ('stress_daydreaming', models.IntegerField(default=0)),
                ('stress_control', models.IntegerField(default=0)),
                ('stress_sad', models.IntegerField(default=0)),
                ('stress_active', models.IntegerField(default=0)),
                ('stress_motivated', models.IntegerField(default=0)),
                ('stress_dissatisfied', models.IntegerField(default=0)),
                ('stress_performance', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UKDemographicsSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=0, help_text=b'Please provide your age (in years).')),
                ('sex', models.CharField(help_text=b'Please indicate your sex.', max_length=1, choices=[(b'N', b'Not Indicated'), (b'M', b'Male'), (b'F', b'Female')])),
                ('education_undergrad', models.CharField(default=b'N', max_length=1)),
                ('education_undergrad_major', models.CharField(default=b'', max_length=100)),
                ('education_undergrad_year', models.CharField(default=b'', max_length=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='USDemographicsSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=0, help_text=b'Please provide your age (in years).')),
                ('sex', models.CharField(help_text=b'Please indicate your sex.', max_length=1, choices=[(b'N', b'Not Indicated'), (b'M', b'Male'), (b'F', b'Female')])),
                ('education_undergrad', models.CharField(default=b'N', max_length=1)),
                ('education_undergrad_major', models.CharField(default=b'', max_length=100)),
                ('education_standing', models.CharField(default=b'', max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nasasystemload',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conceptlistingsurvey',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
