# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='website',
        ),
        migrations.AddField(
            model_name='author',
            name='password',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
