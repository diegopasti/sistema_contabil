# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0021_natureza_juridica'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localizacao',
            name='cep',
        ),
        migrations.DeleteModel(
            name='localizacao',
        ),
    ]
