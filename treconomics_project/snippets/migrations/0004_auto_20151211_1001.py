# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_snippetexitsurvey'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippetexitsurvey',
            name='snip_improve',
            field=models.TextField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snippetexitsurvey',
            name='snip_why',
            field=models.TextField(default=0),
            preserve_default=True,
        ),
    ]
