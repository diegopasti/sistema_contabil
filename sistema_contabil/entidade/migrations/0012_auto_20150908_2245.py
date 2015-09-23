# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0011_auto_20150904_0056'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bairro',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bairro',
            name='municipio',
        ),
        migrations.DeleteModel(
            name='bairro',
        ),
    ]
