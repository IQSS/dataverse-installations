# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetfields', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetFieldType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('advancedsearchfieldtype', models.BooleanField()),
                ('allowcontrolledvocabulary', models.BooleanField()),
                ('allowmultiples', models.BooleanField()),
                ('description', models.TextField(null=True, blank=True)),
                ('displayformat', models.CharField(max_length=255, null=True, blank=True)),
                ('displayoncreate', models.BooleanField()),
                ('displayorder', models.IntegerField(null=True, blank=True)),
                ('facetable', models.BooleanField()),
                ('fieldtype', models.CharField(max_length=255)),
                ('name', models.TextField(null=True, blank=True)),
                ('required', models.BooleanField()),
                ('title', models.TextField(null=True, blank=True)),
                ('watermark', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'datasetfieldtype',
                'managed': False,
            },
        ),
    ]
