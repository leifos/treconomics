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
            name='AnitaConsent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agreed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaDemographicsSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(default=0, help_text=b'Please provide your age (in years).')),
                ('status', models.CharField(default=b'', max_length=100)),
                ('work', models.CharField(default=b'', max_length=100)),
                ('level', models.CharField(default=b'', max_length=3)),
                ('search_freq', models.IntegerField(default=0, help_text=b'How many times per week do you conduct searches for information (please enter a whole number)?')),
                ('search_ability', models.CharField(default=b'', max_length=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaExit1Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ae_use_freq', models.IntegerField(default=0)),
                ('ae_complex', models.IntegerField(default=0)),
                ('ae_easy', models.IntegerField(default=0)),
                ('ae_integrated', models.IntegerField(default=0)),
                ('ae_inconsistent', models.IntegerField(default=0)),
                ('ae_learn_quickly', models.IntegerField(default=0)),
                ('ae_cumbersome', models.IntegerField(default=0)),
                ('ae_confident', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaExit2Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ae_time_extent', models.IntegerField(default=0)),
                ('ae_time_reasonable', models.TextField(default=b'')),
                ('ae_time_process', models.TextField(default=b'')),
                ('ae_time_amount_found', models.TextField(default=b'')),
                ('ae_time_amount_read', models.TextField(default=b'')),
                ('ae_time_pressure_points', models.TextField(default=b'')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaExit3Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ae_speed_compare', models.TextField(default=b'')),
                ('ae_speed_process', models.TextField(default=b'')),
                ('ae_speed_amount_found', models.TextField(default=b'')),
                ('ae_speed_amount_read', models.TextField(default=b'')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaPostTask0Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_satisfied_amount', models.IntegerField(default=0)),
                ('apt_satisfied_steps', models.IntegerField(default=0)),
                ('apt_work_fast', models.IntegerField(default=0)),
                ('apt_difficult_enough', models.IntegerField(default=0)),
                ('apt_time_pressure', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaPostTask1Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_search_diff', models.IntegerField(default=0)),
                ('apt_hurried', models.IntegerField(default=0)),
                ('apt_satisfied_systems', models.IntegerField(default=0)),
                ('apt_doing_well', models.IntegerField(default=0)),
                ('apt_found_enough', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaPostTask2Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_accurate', models.IntegerField(default=0)),
                ('apt_quick_results', models.IntegerField(default=0)),
                ('apt_more_info', models.IntegerField(default=0)),
                ('apt_time_left', models.IntegerField(default=0)),
                ('apt_quick_task', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaPostTask3Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_system_relevance', models.IntegerField(default=0)),
                ('apt_system_download', models.IntegerField(default=0)),
                ('apt_finding_diff', models.IntegerField(default=0)),
                ('apt_all_info', models.IntegerField(default=0)),
                ('apt_task_diff', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnitaPreTaskSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('apt_interested', models.IntegerField(default=0)),
                ('apt_know', models.IntegerField(default=0)),
                ('apt_clear_what', models.IntegerField(default=0)),
                ('apt_info_diff', models.IntegerField(default=0)),
                ('apt_sys_diff', models.IntegerField(default=0)),
                ('apt_clear_how', models.IntegerField(default=0)),
                ('apt_clear_steps', models.IntegerField(default=0)),
                ('apt_difficult_finish', models.IntegerField(default=0)),
                ('apt_task_diff', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MickeyPostTaskSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('snip_helpfulness', models.IntegerField(default=0)),
                ('serp_simplicity', models.IntegerField(default=0)),
                ('snip_informativeness', models.IntegerField(default=0)),
                ('serp_confusion', models.IntegerField(default=0)),
                ('snip_clarity', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
