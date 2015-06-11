# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=100)),
                ('slug', models.SlugField(default=b'slug')),
                ('library', models.ForeignKey(to='main.Library', null=True)),
            ],
        ),
    ]
