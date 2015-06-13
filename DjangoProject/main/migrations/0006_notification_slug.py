# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_notification_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='slug',
            field=models.CharField(default=b'default', max_length=100),
        ),
    ]
