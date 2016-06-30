# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metadatablock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('displayname', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'metadatablock',
                'managed': False,
            },
        ),
    ]
