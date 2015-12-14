# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0005_auto_20151213_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='age',
            field=models.IntegerField(help_text=b'Please provide your age (in years).'),
        ),
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='news_search_freq',
            field=models.IntegerField(help_text=b'How often do you search the web for news articles?'),
        ),
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='search_freq',
            field=models.IntegerField(help_text=b'How often do you search the web?'),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_easy',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_help',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_improve',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_info',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_prefer',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_useful',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetexitsurvey',
            name='snip_why',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='serp_confusion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='serp_simplicity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='snip_clarity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='snip_distracting',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='snip_helpfulness',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='snip_informativeness',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='snip_usefulness',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='task_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='snippetposttasksurvey',
            name='topic_num',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='ae_confident',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='ae_cumbersome',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='apt_accurate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='apt_hurried',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='apt_quick_results',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='apt_satisfied_systems',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='apt_search_diff',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='task_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='systemsnippetposttasksurvey',
            name='topic_num',
            field=models.IntegerField(),
        ),
    ]
