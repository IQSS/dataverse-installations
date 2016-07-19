# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dvobjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datafile',
            fields=[
                ('id', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='dvobjects.DvObject')),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('contenttype', models.CharField(max_length=255)),
                ('filesystemname', models.CharField(max_length=255)),
                ('filesize', models.BigIntegerField(null=True, blank=True)),
                ('ingeststatus', models.CharField(max_length=1, null=True, blank=True)),
                ('md5', models.CharField(max_length=255)),
                ('restricted', models.BooleanField()),
            ],
            options={
                'db_table': 'datafile',
                'managed': False,
            },
        ),
    ]
