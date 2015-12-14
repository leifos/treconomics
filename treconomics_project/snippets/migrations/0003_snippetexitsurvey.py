# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0002_snippetdemographicssurvey_snippetposttasksurvey_systemsnippetposttasksurvey'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnippetExitSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snip_info', models.IntegerField(default=0)),
                ('snip_easy', models.IntegerField(default=0)),
                ('snip_help', models.IntegerField(default=0)),
                ('snip_useful', models.IntegerField(default=0)),
                ('snip_prefer', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
