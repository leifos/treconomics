# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnippetDemographicsSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=0, help_text=b'Please provide your age (in years).')),
                ('sex', models.CharField(help_text=b'Please indicate your sex.', max_length=1, choices=[(b'N', b'Not Indicated'), (b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')])),
                ('work', models.CharField(default=b'', max_length=100)),
                ('level', models.CharField(default=b'', max_length=3)),
                ('search_freq', models.IntegerField(default=-1, help_text=b'How often do you search the web?')),
                ('news_search_freq', models.IntegerField(default=-1, help_text=b'How often do you search the web for news articles?')),
                ('input_device', models.CharField(default=b'', max_length=2)),
                ('search_engine', models.CharField(default=b'', max_length=3)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnippetPostTaskSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('snip_helpfulness', models.IntegerField(default=0)),
                ('serp_simplicity', models.IntegerField(default=0)),
                ('snip_distracting', models.IntegerField(default=0)),
                ('snip_informativeness', models.IntegerField(default=0)),
                ('serp_confusion', models.IntegerField(default=0)),
                ('snip_clarity', models.IntegerField(default=0)),
                ('snip_usefulness', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemSnippetPostTaskSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_accurate', models.IntegerField(default=0)),
                ('apt_quick_results', models.IntegerField(default=0)),
                ('apt_search_diff', models.IntegerField(default=0)),
                ('apt_hurried', models.IntegerField(default=0)),
                ('apt_satisfied_systems', models.IntegerField(default=0)),
                ('ae_cumbersome', models.IntegerField(default=0)),
                ('ae_confident', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
