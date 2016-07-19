# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dvobjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='dvobjects.DvObject')),
                ('authority', models.CharField(max_length=255, null=True, blank=True)),
                ('doiseparator', models.CharField(max_length=255, null=True, blank=True)),
                ('fileaccessrequest', models.BooleanField()),
                ('globalidcreatetime', models.DateTimeField(null=True, blank=True)),
                ('identifier', models.CharField(max_length=255)),
                ('protocol', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'dataset',
                'managed': False,
            },
        ),
    ]
