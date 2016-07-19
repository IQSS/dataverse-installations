# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0005_datasetfieldvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetFieldControlledVocabularyValue',
            fields=[
                ('datasetfield', models.ForeignKey(primary_key=True, serialize=False, to='datasetfields.DatasetField')),
            ],
            options={
                'db_table': 'datasetfield_controlledvocabularyvalue',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='controlledvocabularyvalue',
            options={'ordering': ('displayorder',), 'managed': False},
        ),
    ]
