# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0003_controlledvocabularyvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'datasetfield',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DatasetFieldCompoundValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayorder', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'datasetfieldcompoundvalue',
                'managed': False,
            },
        ),        
    ]
