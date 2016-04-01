# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidade', '0007_auto_20150903_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_ibge', models.CharField(unique=True, max_length=7, verbose_name=b'C\xc3\xb3digo Munic\xc3\xadpal:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name=b'Munic\xc3\xadpio:', error_messages={b'required': b'Campo Obrigat\xc3\xb3rio!', b'invalid': b'Formato Inv\xc3\xa1lido!'})),
                ('estado', models.ForeignKey(to='entidade.estado')),
            ],
        ),
    ]
