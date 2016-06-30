# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLogRecord',
            fields=[
                ('id', models.CharField(max_length=36, serialize=False, primary_key=True)),
                ('actionresult', models.CharField(max_length=255, null=True, blank=True)),
                ('actionsubtype', models.CharField(max_length=255, null=True, blank=True)),
                ('actiontype', models.CharField(max_length=255, null=True, blank=True)),
                ('endtime', models.DateTimeField(null=True, blank=True)),
                ('info', models.CharField(max_length=1024, null=True, blank=True)),
                ('starttime', models.DateTimeField(null=True, blank=True)),
                ('useridentifier', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-starttime',),
                'db_table': 'actionlogrecord',
                'managed': False,
            },
        ),
    ]
