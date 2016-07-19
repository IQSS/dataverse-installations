# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20160628_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'managed': False},
        ),
    ]
