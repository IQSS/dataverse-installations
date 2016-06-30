# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0004_datasetfield_datasetfieldcompoundvalue_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetFieldValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayorder', models.IntegerField(null=True, blank=True)),
                ('value', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'datasetfieldvalue',
                'managed': False,
            },
        ),
    ]
