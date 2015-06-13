# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_notification_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='book',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='library',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
