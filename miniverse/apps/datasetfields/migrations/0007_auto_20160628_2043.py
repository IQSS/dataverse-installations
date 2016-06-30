# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0006_auto_20160628_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datasetfield',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='datasetfieldcompoundvalue',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='datasetfieldcontrolledvocabularyvalue',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='datasetfieldtype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='datasetfieldvalue',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='metadatablock',
            options={'managed': False},
        ),
    ]
