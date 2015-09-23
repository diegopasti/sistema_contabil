# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0016_auto_20150914_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contato',
            name='ddd',
        ),
        migrations.AlterField(
            model_name='contato',
            name='numero',
            field=models.CharField(max_length=20, verbose_name=b'Numero:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='cep',
            field=models.CharField(unique=True, max_length=8, verbose_name=b'C\xc3\xb3digo Postal:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='nome',
            field=models.CharField(max_length=100, verbose_name=b'Endere\xc3\xa7o:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
        migrations.AlterField(
            model_name='localizacao',
            name='complemento',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Complemento:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'}),
        ),
    ]
