# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20151211_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='input_device',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='level',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='search_engine',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='snippetdemographicssurvey',
            name='work',
            field=models.CharField(max_length=100),
        ),
    ]
