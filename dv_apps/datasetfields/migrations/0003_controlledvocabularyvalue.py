# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0002_datasetfieldtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlledVocabularyValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strvalue', models.TextField()),
                ('identifier', models.CharField(max_length=255, null=True, blank=True)),
                ('displayorder', models.IntegerField()),
            ],
            options={
                'db_table': 'controlledvocabularyvalue',
                'managed': False,
            },
        ),
    ]
