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
            name='DocumentsExamined',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('docid', models.CharField(max_length=30)),
                ('doc_num', models.CharField(max_length=30)),
                ('judgement', models.IntegerField()),
                ('judgement_date', models.DateTimeField(verbose_name=b'Date Examined')),
                ('url', models.CharField(max_length=200)),
                ('task', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_num', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicQuerySuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_num', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=40)),
                ('link', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.CharField(max_length=200, null=True, blank=True)),
                ('experiment', models.IntegerField(default=0)),
                ('condition', models.IntegerField(default=0)),
                ('rotation', models.IntegerField(default=0)),
                ('tasks_completed', models.IntegerField(default=0)),
                ('steps_completed', models.IntegerField(default=0)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
