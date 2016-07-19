# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_datasetversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datasetversion',
            options={'ordering': ('-id',), 'managed': False},
        ),
    ]
