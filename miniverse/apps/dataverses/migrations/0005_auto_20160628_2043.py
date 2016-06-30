# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataverses', '0004_auto_20160628_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataverse',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='dataverserole',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='dataversetheme',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'managed': False},
        ),
    ]
