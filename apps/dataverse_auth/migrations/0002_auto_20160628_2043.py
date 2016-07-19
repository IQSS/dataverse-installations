# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataverse_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apitoken',
            options={'ordering': ('-expiretime', 'authenticateduser'), 'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authenticateduser',
            options={'ordering': ('useridentifier',), 'managed': False},
        ),
    ]
