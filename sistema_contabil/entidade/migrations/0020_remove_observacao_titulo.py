# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0019_observacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observacao',
            name='titulo',
        ),
    ]
