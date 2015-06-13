# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150611_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='owner',
        ),
    ]
