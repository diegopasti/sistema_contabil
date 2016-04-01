# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0006_contato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='regiao',
            field=models.CharField(max_length=20, verbose_name=b'Regi\xc3\xa3o:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
